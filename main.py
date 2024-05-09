import os
import csv
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import re

def read_config(config_file):
    """
    Read configuration from a text file.
    """
    input_folder = ""
    output_file = ""
    try:
        with open(config_file, 'r') as file:
            for line in file:
                if line.startswith("input_folder"):
                    input_folder = re.search(r'=(.*)', line).group(1).strip()
                elif line.startswith("output_file"):
                    output_file = re.search(r'=(.*)', line).group(1).strip()
    except Exception as e:
        print(f"Error reading configuration file: {e}")
    return input_folder, output_file


def perform_ocr(image):
    """
    Perform OCR on the image using Tesseract OCR.
    """
    try:
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image, lang='hrv')
        return extracted_text.strip()
    except Exception as e:
        print(f"Error performing OCR: {e}")
        return ""

def process_pdf(pdf_path):
    """
    Process PDF file: extract text using PyMuPDF.
    If the text is empty, convert PDF to images and perform OCR again.
    """
    try:
        # Extract text using PyMuPDF
        with fitz.open(pdf_path) as pdf_document:
            extracted_text = ""
            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)
                page_text = page.get_text()
                extracted_text += page_text
        if extracted_text.strip():
            return extracted_text.strip()
        else:
            # Convert PDF to images
            images = convert_pdf_to_images(pdf_path)
            # Perform OCR on each image using Tesseract
            return perform_ocr_on_images(images)
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return ""

def convert_pdf_to_images(pdf_path):
    """
    Convert PDF to a list of PIL images.
    """
    try:
        images = []
        with fitz.open(pdf_path) as pdf_document:
            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)
                pix = page.get_pixmap()
                mode = "RGB" if pix.n == 3 else "L"
                image = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                images.append(image)
        return images
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []

def perform_ocr_on_images(images):
    """
    Perform OCR on a list of images using Tesseract OCR.
    """
    extracted_text = ""
    for image in images:
        try:
            text = perform_ocr(image)
            extracted_text += text + "\n"
        except Exception as e:
            print(f"Error performing OCR on image: {e}")
    return extracted_text.strip()

def process_image(image_path):
    """
    Process image file: extract text using OCR.
    """
    try:
        # Use pytesseract to perform OCR on the image
        with Image.open(image_path) as image:
            extracted_text = perform_ocr(image)
        return extracted_text
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""

def extract_information(text):
    """
    Extract invoice number, date, and amount from OCR text.
    """
    # Define patterns for invoice number variations
    invoice_patterns = [
        r"Račun\s*broj:\s*([0-9A-Za-z-/]+)",
        r"Račun\s*br[.]*:\s*([0-9A-Za-z-/]+)",
        r"računa\s*broj\s*([0-9A-Za-z-/]+)",
        r"RAČUN\s*br[.]*\s*([0-9A-Za-z-/]+)"
    ]
    
    # Define date patterns
    date_patterns = [
        r"Datum\s*računa:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Datum:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Datum\s*i\s*vrijeme:\s*(\d{1,2}\.\d{1,2}\.\d{4})",
        r"Datum\s*dokumenta:\s*(\d{2}\.\d{2}\.\d{4})",
        r"Datum\s*izdavanja:\s*(\d{2}\.\d{2}\.\d{4})",
        r"dana\s*(\d{2}\.\d{2}\.\d{4})",
        r"datum\s*izdavanja:\s*.*?(\d{1,2}\.\d{1,2}\.\d{4})",
        r"\d{1,2}\.\d{1,2}\.\d{4}",
        r"Issue\s*date:\s*(\d{2}/\d{2}/\d{4})"
    ]

    # Define amount patterns
    amount_patterns = [
        r"Ukupan\s*iznos\s*naplate:\s*(\d+,\d+)\s*€",
        r"TOTAL\s*\(\w+\):\s*€(\d+,\d+\.\d{2})",
        r"UKUPNO:\s*(\d+,\d+)\s*(EUR|€)",
        r"Amount\s*paid\s*\(\w+\)\s*€\s*(\d+,\d+\.\d{2})",
        r"Za\s*uplatu\s*(EUR|€):\s*(\d+,\d+)",
        r"Ukupan\s*iznos\s*za\s*plaćanje\s*(\d+,\d+)\s*(EUR|€)",
        r"Ukupno\s*([\d,]+\s*(EUR|€))",
        r"Sveukupno\s*\(\w+:\s*[\d,]+\)\s*(\d+,\d+)\s*(EUR|€)",
        r"Iznos\s*([\d,]+)",
        r"UKUPNO\s*IZNOS:\s*\w+\s*=\s*([\d,]+)\s*(EUR|€)\s*\w+\s*=\s*([\d,]+)"
    ]

    # Find invoice number
    invoice = ""
    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            invoice = match.group(1)
            break

    # Find date
    date = ""
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date = match.group(1)
            break

    # Find amount
    amount = ""
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(0)
            break

    return invoice, date, amount

def process_files(input_folder, output_file):
    """
    Process files in the input folder: perform OCR on PDFs and images,
    and extract invoice number, date, and amount.
    """
    results = []
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        if file_name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            try:
                if file_name.lower().endswith('.pdf'):
                    # Handle PDF files using PyMuPDF
                    extracted_text = process_pdf(file_path)
                else:
                    # Handle image files
                    extracted_text = process_image(file_path)
                
                invoice, date, amount = extract_information(extracted_text)
                results.append((file_name, extracted_text, invoice, date, amount))
            except Exception as e:
                # Handle exceptions by adding filename to results with empty text
                print(f"Error processing {file_name}: {e}")
                results.append((file_name, "", "", "", ""))
    # Save extracted text and information to CSV file
    save_to_csv(results, output_file)

def save_to_csv(data, output_file):
    """
    Save extracted text and information to CSV file.
    """
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['File Name', 'Extracted Text', 'Invoice', 'Date', 'Amount'])
            for row in data:
                csv_writer.writerow(row)
        print(f"Extracted text and information saved to {output_file}")
    except Exception as e:
        print(f"Error saving to CSV file: {e}")

def main():
    # Read configuration from config.txt
    config_file = "config.txt"
    input_folder, output_file = read_config(config_file)
    # Process files in the input folder
    process_files(input_folder, output_file)

if __name__ == "__main__":
    main()
