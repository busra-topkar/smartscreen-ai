from pathlib import Path

from pypdf import PdfReader
from docx import Document


def _read_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def _read_docx(file_path):
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text:
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def read_cv(file_path):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        text = _read_pdf(file_path)

    elif extension == ".docx":
        text = _read_docx(file_path)

    else:
        raise ValueError("Sadece PDF ve DOCX dosyaları desteklenmektedir.")

    text = " ".join(text.split())

    return text