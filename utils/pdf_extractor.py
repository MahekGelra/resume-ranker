import PyPDF2


def extract_text_from_pdf(pdf_file):
    """
    Extracts and returns all text content from a PDF file.

    Parameters:
        pdf_file: A file-like object (e.g., from open() or Streamlit's uploader)

    Returns:
        str: The extracted text, or an empty string if extraction fails.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""