import os
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
import pickle
from config import api_key as apiKey
# --- Configuration ---
# It's recommended to set your API key as an environment variable for security.
# If the environment variable is not set, the code will prompt you to enter it.

genai.configure(api_key=apiKey)

PROMPT_TEMPLATES = {

    "solution": """
Sen bir lise {grade}. sınıf öğretmenisin. Aşağıda verilen konu bilgisi ve öğrencinin önceki konuşmalarına göre, öğrencinin sorduğu sorunun çözümünü adım adım, anlaşılır ve kısa cümlelerle açıkla. Gereksiz selamlaşma veya sohbet ifadeleri ekleme. Eğer işlem basamakları varsa, her adımı numaralandır. Yanıtın sonunda sonucu özetle.

Önceki Konuşmalar:
{history_text}

Konu Bilgisi:
{context}

Soru:
{question}

Yanıt:
""",

    "example": """Sen bir lise {grade}. sınıf öğretmenisin. Aşağıda verilen konu bilgisi ve öğrencinin önceki 
    konuşmalarına göre, öğrencinin sorduğu kavramla ilgili kısa, açık ve seviyeye uygun bir örnek ver. Gerekirse 
    örneği açıklayarak anlaşılır hale getir. Gereksiz selamlaşma veya sohbet ifadeleri ekleme. Eğer soru istenmiş ise 
    yazdığın sorunun çözümünü de yaz. 

Önceki Konuşmalar:
{history_text}

Konu Bilgisi:
{context}

Soru:
{question}

Yanıt:
""",
    "definition": """
Sen bir lise {grade}. sınıf öğretmenisin. Aşağıda verilen konu bilgisi ve öğrencinin önceki konuşmalarına göre, öğrencinin sorduğu terimi veya kavramı açık, sade ve kısa bir şekilde tanımla. Gereksiz selamlaşma veya sohbet ifadeleri ekleme. Tanımda, öğrencinin seviyesine uygun, anlaşılır bir dil kullan. Gerekirse örnekle destekle.

Önceki Konuşmalar:
{history_text}

Konu Bilgisi:
{context}

Soru:
{question}

Yanıt:
""",

    "comparison": """
Sen bir lise {grade}. sınıf öğretmenisin. Aşağıda verilen konu bilgisi ve öğrencinin önceki konuşmalarına göre, öğrencinin sorduğu iki veya daha fazla kavramı kısa, açık ve net şekilde kıyasla. Farklılıklarını ve benzerliklerini maddeler halinde, anlaşılır bir dille belirt. Gereksiz selamlaşma veya sohbet ifadeleri kullanma.

Önceki Konuşmalar:
{history_text}

Konu Bilgisi:
{context}

Soru:
{question}

Yanıt:
"""
,
    "categorization": """
Sen bir lise {grade}. sınıf öğretmenisin. Aşağıda verilen konu bilgisi ve öğrencinin önceki konuşmalarına göre, öğrencinin verdiği öğeleri veya kavramları anlamlı şekilde sınıflandır. Sınıflandırma ölçütünü açıkla ve her bir grubu kısa ama anlaşılır şekilde tanımla. Gereksiz selamlaşma veya sohbet ifadeleri ekleme.

Önceki Konuşmalar:
{history_text}

Konu Bilgisi:
{context}

Soru:
{question}

Yanıt:
"""
}


# --- Model and Index Loading ---
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("faiss_index.idx")
with open("documents.pkl", "rb") as f:
    documents, file_names = pickle.load(f)


def retrieve_context(question: str, top_k=1) -> str:
    """
    Retrieves the most relevant context for a given question using a FAISS index.
    """
    q_vec = model.encode([question])
    D, I = index.search(q_vec, top_k)
    return "\n\n".join([documents[i] for i in I[0]])


def generate_with_gemini(context: str, question: str, grade: int, history_text: str, intent: str) -> str:
    prompt = PROMPT_TEMPLATES.get(intent, "").format(
        grade=grade,
        history_text=history_text or "Yok",
        context=context,
        question=question
    )
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
    response = gemini_model.generate_content(prompt)
    return response.text.strip()
