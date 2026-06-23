from io import BytesIO

from pypdf import PdfReader

from docx import Document


def load_document(
    filename: str,
    file_bytes: bytes
):

    extension = (
        filename
        .split(".")[-1]
        .lower()
    )

    print(
        f"Loading File Type: {extension}"
    )

    if extension == "txt":

        return file_bytes.decode(
            "utf-8"
        )

    elif extension == "pdf":

        return extract_pdf_text(
            file_bytes
        )

    elif extension == "docx":

        return extract_docx_text(
            file_bytes
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def extract_pdf_text(
    file_bytes: bytes
):

    pdf = PdfReader(
        BytesIO(file_bytes)
    )

    text = ""

    for page in pdf.pages:

        page_text = (
            page.extract_text()
        )

        if page_text:

            text += page_text + "\n"

    return text


def extract_docx_text(
    file_bytes: bytes
):

    doc = Document(
        BytesIO(file_bytes)
    )

    return "\n".join(
        para.text
        for para in doc.paragraphs
    )