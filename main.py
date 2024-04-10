import os
import csv
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# Input folder directory
input_folder = r"F:\Python\jati-python-ocr-demo\ov"
# Output CSV file name and location
output_file = r"F:\Python\jati-python-ocr-demo\output.csv"

def perform_ocr(image):
    """
    Perform OCR on the image using Tesseract OCR.
    """
    try:
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        print(f"Error performing OCR: {e}")
        return ""

def process_pdf(pdf_path):
    """
    Process PDF file: extract text using PyMuPDF.
    """
    try:
        extracted_text = ""
        with fitz.open(pdf_path) as pdf_document:
            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)
                page_text = page.get_text()
                extracted_text += page_text
        return extracted_text.strip()
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return ""

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

def process_files(input_folder, output_file):
    """
    Process files in the input folder: perform OCR on PDFs and images.
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
                results.append((file_name, extracted_text))
            except Exception as e:
                # Handle exceptions by adding filename to results with empty text
                print(f"Error processing {file_name}: {e}")
                results.append((file_name, ""))
    # Save extracted text to CSV file
    save_to_csv(results, output_file)

def save_to_csv(data, output_file):
    """
    Save extracted text to CSV file.
    """
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['File Name', 'Extracted Text'])
            for file_name, text in data:
                csv_writer.writerow([file_name, text])
        print(f"Extracted text saved to {output_file}")
    except Exception as e:
        print(f"Error saving to CSV file: {e}")

def main():
    # Process files in the input folder
    process_files(input_folder, output_file)


if __name__ == "__main__":
    main()
