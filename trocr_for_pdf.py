import os
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import pdfplumber
import fitz

def get_pdf_page_count(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)

def fix_cropbox(pdf_path):
    """Fix missing CropBox by setting it to MediaBox and save a new PDF."""
    doc = fitz.open(pdf_path)
    for page in doc:
        media_box = page.mediabox  # Get MediaBox
        # crop_box = page.cropbox  # Get existing CropBox

        # If CropBox is missing or incorrect, set it to match MediaBox
        # if crop_box is None or not media_box.contains(crop_box):
        #     print(f"Fixing CropBox for Page {page.number + 1}")
        page.set_cropbox(media_box)
    fixed_pdf_path = "fixed_" + os.path.basename(pdf_path)
    fixed_pdf_path = os.path.join(os.path.dirname(pdf_path), fixed_pdf_path)
    doc.save(fixed_pdf_path)  # Save the fixed PDF
    doc.close()
    print(f"CropBox fixed and saved as: {fixed_pdf_path}")
    return fixed_pdf_path  # Return new file path
# # Set up Tesseract Path (For Windows, update the path accordingly)
# if os.name == "nt":  # Windows
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# else:  # Linux/macOS (Tesseract should be in system PATH)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def extract_text_from_page(pdf_path, page_number):
    """Extracts text from a single PDF page using OCR."""
    try:
        images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)
        if images:
            return pytesseract.image_to_string(images[0])
    except Exception as e:
        print(f"Error extracting text from page {page_number + 1}: {e}")
    return "No text extracted."

# Function to extract tables from a single page
def extract_tables_from_page(pdf_path, page_number=0):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_number < len(pdf.pages):
                return pdf.pages[page_number].extract_tables()  # Extract multiple tables
    except Exception as e:
        print(f"Error extracting tables from page {page_number + 1}: {e}")
    return None

# Example Usage
pdf_path = "/Users/muzammilmohammad/Desktop/CA chatbot/tax_docs/Income Tax Act 1961 Amended 2024.pdf"  # Replace with your PDF file path
pdf_path = fix_cropbox(pdf_path)
page_to_process = 0  # Page number (0-based)
page_count=get_pdf_page_count(pdf_path)
# Get the PDF filename without extension
pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

# Define the output folder for this PDF
output_folder = os.path.join("/Users/muzammilmohammad/Desktop/CA chatbot/pdf_data", pdf_name)
tables_folder = os.path.join(output_folder, "tables")

# Create necessary folders
os.makedirs(output_folder, exist_ok=True)
os.makedirs(tables_folder, exist_ok=True)

while(page_to_process<page_count):


# Extract text and save
    extracted_text = extract_text_from_page(pdf_path, page_to_process)
    text_file_path = os.path.join(output_folder, f"page_{page_to_process + 1}_text.txt")
    with open(text_file_path, "w", encoding="utf-8") as f:
       f.write(extracted_text)

# Extract tables and save each one separately
    tables = extract_tables_from_page(pdf_path, page_to_process)
    if tables:
        for i, table in enumerate(tables):
            df = pd.DataFrame(table)
            table_file_path = os.path.join(tables_folder, f"page_{page_to_process + 1}_table_{i + 1}.csv")
            df.to_csv(table_file_path, index=False)
            print(f"Table {i + 1} saved to: {table_file_path}")

# Print results
    print(f"Extracted text saved to: {text_file_path}")
    if tables:
        print(f"Extracted tables saved in: {tables_folder}")
    else:
        print("No tables found on this page.")
    page_to_process+=1
