import os
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
import pickle

# --- Configuration ---
# It's recommended to set your API key as an environment variable for security.
# If the environment variable is not set, the code will prompt you to enter it.

genai.configure(api_key="API_KEY")

# --- Model and Index Loading ---
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("script/faiss_index.idx")
with open("script/documents.pkl", "rb") as f:
    documents, file_names = pickle.load(f)

def retrieve_context(question: str, top_k=1) -> str:
    """
    Retrieves the most relevant context for a given question using a FAISS index.
    """
    q_vec = model.encode([question])
    D, I = index.search(q_vec, top_k)
    return "\n\n".join([documents[i] for i in I[0]])

def generate_with_gemini(context: str, question: str) -> str:
    """
    Generates a response using the Gemini 2.0 Flash model.
    """
    prompt = f"""
Sen bir lise öğretmenisin. Aşağıdaki konu bilgisine göre, öğrencinin sorusuna basit ve açık bir şekilde cevap ver.

Konu Bilgisi:
{context}

Soru:
{question}

Yanıt:
"""

    # Initialize the Gemini model
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')

    # Generate content
    response = gemini_model.generate_content(prompt)

    return response.text.strip()