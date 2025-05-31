import pdfplumber
import os
from pathlib import Path


def extract_text_with_layout(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def process_pdfs_in_paths(paths):
    for path_str in paths:
        path = Path(path_str)
        if not path.exists() or not path.is_dir():
            print(f"Invalid path: {path}")
            continue

        for pdf_file in path.rglob("*.pdf"):
            print(f"Processing: {pdf_file}")
            text = extract_text_with_layout(pdf_file)
            txt_file = pdf_file.with_suffix('.txt')
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved as: {txt_file}")


# Example usage
paths = [
    "C:/Users/ahmet/PycharmProjects/tutorbot-backend/kaynaks/biyoloji",
    "C:/Users/ahmet/PycharmProjects/tutorbot-backend/kaynaks/basic-kimya",
    "C:/Users/ahmet/PycharmProjects/tutorbot-backend/kaynaks/basic-math"
]

process_pdfs_in_paths(paths)