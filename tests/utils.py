from docx import Document


def extract_document_text(path: str) -> str:
    document = Document(path)
    parts = []
    for paragraph in document.paragraphs:
        runs = paragraph.runs
        for i in range(len(runs)):
            parts.append(runs[i].text)
    return " ".join(parts)
