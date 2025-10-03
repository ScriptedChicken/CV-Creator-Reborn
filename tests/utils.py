from io import BytesIO

import requests
from docx import Document

def text_to_document(text:str):
    doc = Document()
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        if paragraph.strip():  # Only add non-empty paragraphs
            doc.add_paragraph(paragraph)
    return doc

def text_to_docx_response_simple(text, filename="document.docx"):
    doc = text_to_document(text)
    docx_buffer = BytesIO()
    doc.save(docx_buffer)
    docx_content = docx_buffer.getvalue()
    docx_buffer.close()

    response = requests.models.Response()
    response.status_code = 200
    response.headers["Content-Type"] = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    response._content = docx_content

    return response
