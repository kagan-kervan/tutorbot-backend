from transformers import pipeline
import os
from pathlib import Path

def advanced_summary(text):
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']


#Eğer gelişmiş özetleme isterseniz nltk veya transformers kullanılabilir.
def simple_summary(text, max_sentences=3):
    sentences = text.replace("\n", " ").split(".")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return ". ".join(sentences[:max_sentences]) + "."

def summarize_folder(folder_path, output_path="summaries.txt"):
    summaries = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                summary = advanced_summary(content)
                summaries.append(f"--- {filename} ---\n{summary}\n")
            with open(file_path+"_sum", "w", encoding="utf-8") as out_file:
                out_file.write(summary)
            print(f"{len(file_path)} dosya özetlendi ve yazıldı.")

    # Özetleri bir dosyaya yaz
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write("\n".join(summaries))

    print(f"{len(summaries)} dosya özetlendi ve '{output_path}' dosyasına yazıldı.")


summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")
# Kullanım:
summarize_folder("documents")  # klasör adını kendine göre değiştir