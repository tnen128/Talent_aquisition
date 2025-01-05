import streamlit as st
import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF for PDF parsing

def extract_text_from_pdf(file_path: str) -> str:
    text_content = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text_content += page.get_text()
    return text_content

def extract_text_with_ocr(file_path: str) -> str:
    # Example for OCR on image-based PDFs
    text_content = ""
    with fitz.open(file_path) as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text_content += pytesseract.image_to_string(img)
    return text_content

def process_cvs():
    st.header("Process CVs")
    directory = st.text_input("Enter directory path of CVs")

    if st.button("Process"):
        if not directory or not os.path.isdir(directory):
            st.error("Please enter a valid directory.")
            return

        processed_count = 0
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.lower().endswith(".pdf"):
                # Attempt direct extraction
                text = extract_text_from_pdf(file_path)
                
                # If direct extraction fails or is empty, try OCR
                if len(text.strip()) < 10:
                    text = extract_text_with_ocr(file_path)

                # Save or queue text for embedding
                st.write(f"Extracted text for {filename[:50]}... (Length: {len(text)})")
                # TODO: Call embedding function or store text for batch embedding

                processed_count += 1
            # Add docx or other format handlers if needed
        st.success(f"Processed {processed_count} CV(s).")
