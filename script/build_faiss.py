from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

# Embed modeli
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Belgeleri oku
doc_folder = "../documents"
documents = []
file_names = []

for file in os.listdir(doc_folder):
    path = os.path.join(doc_folder, file)
    with open(path, encoding="utf-8") as f:
        content = f.read()
        documents.append(content)
        file_names.append(file)

# Embed üret
embeddings = model.encode(documents)

# FAISS index oluştur
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(embeddings)

# Kaydet
faiss.write_index(index, "../faiss_index.idx")
with open("../documents.pkl", "wb") as f:
    pickle.dump((documents, file_names), f)
