import os
import csv
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def process_image(image_path):
    """
    Process image using Tesseract OCR.
    """
    try:
        # Open image using PIL
        image = Image.open(image_path)
        # Use pytesseract to extract text from image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""

def process_pdf(pdf_path):
    """
    Process PDF using PyMuPDF.
    """
    results = []
    try:
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            page_text = page.get_text()
            results.append(page_text.strip())
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
    return results

def process_files(folder_path):
    """
    Process PDFs and images in the specified folder.
    """
    results = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if file_name.endswith('.pdf'):
                # Handle PDF files using PyMuPDF
                extracted_text = process_pdf(file_path)
                for text in extracted_text:
                    results.append((file_name, text))
            elif file_name.endswith(('.jpg', '.jpeg', '.png')):
                # Process images using Pillow and Tesseract OCR
                extracted_text = process_image(file_path)
                if extracted_text:
                    results.append((file_name, extracted_text))
            else:
                print(f"Unsupported file format: {file_name}")
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    return results

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
    # Relative folder path
    folder_path = 'ov'
    # Output CSV file path
    output_file = 'output.csv'

    # Process files in the folder
    extracted_text = process_files(folder_path)

    # Save extracted text to CSV file
    save_to_csv(extracted_text, output_file)

if __name__ == "__main__":
    main()
