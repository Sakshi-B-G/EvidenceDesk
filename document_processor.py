
from pypdf import PdfReader
from io import BytesIO
import re


def extract_document(uploaded_file):
    """
    Extract text from a PDF or TXT file.

    Returns a list of records containing:
    document name, page number, and extracted text.
    """
    filename = uploaded_file.name
    extension = filename.lower().rsplit(".", 1)[-1]
    pages = []

    if extension == "pdf":
        pdf = PdfReader(BytesIO(uploaded_file.getvalue()))

        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                pages.append({
                    "document_name": filename,
                    "page_number": page_number,
                    "text": text.strip()
                })

    elif extension == "txt":
        raw_text = uploaded_file.getvalue().decode(
            "utf-8", errors="replace"
        )

        if raw_text.strip():
            pages.append({
                "document_name": filename,
                "page_number": 1,
                "text": raw_text.strip()
            })

    else:
        raise ValueError("Only PDF and TXT files are supported.")

    if not pages:
        raise ValueError(
            "No readable text found. The PDF may be scanned "
            "or the document may be empty."
        )

    return pages


def split_into_passages(pages, max_words=220, overlap_words=40):
    """
    Split extracted text into smaller overlapping passages.

    Overlap helps preserve context between neighbouring passages.
    """
    if max_words <= 0:
        raise ValueError("max_words must be greater than zero.")

    if overlap_words < 0 or overlap_words >= max_words:
        raise ValueError(
            "overlap_words must be non-negative and smaller "
            "than max_words."
        )

    passages = []
    passage_number = 1
    step = max_words - overlap_words

    for page in pages:
        words = re.findall(r"\S+", page["text"])

        for start in range(0, len(words), step):
            chunk_words = words[start:start + max_words]

            if not chunk_words:
                break

            passages.append({
                "passage_id": f"P{passage_number}",
                "document_name": page["document_name"],
                "page_number": page["page_number"],
                "text": " ".join(chunk_words)
            })

            passage_number += 1

            if start + max_words >= len(words):
                break

    return passages
