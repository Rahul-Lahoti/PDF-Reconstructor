import pytesseract
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import os
import tempfile

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    page_texts = []
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        page_texts.append((i, text))
    return page_texts

def process_pdf(pdf_path):
    try:
        # Extract text from each page
        page_texts = extract_text_from_pdf(pdf_path)
        
        # Sort based on first 20 chars of text (naive ordering logic)
        sorted_pages = sorted(page_texts, key=lambda x: x[1][:20])
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for idx, _ in sorted_pages:
            writer.add_page(reader.pages[idx])
        
        # Save reordered PDF
        output_path = os.path.join(tempfile.gettempdir(), "reordered.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        
        reasoning = "Pages reordered based on alphabetical order of their extracted text."
        return output_path, reasoning
    
    except Exception as e:
        return None, str(e)
