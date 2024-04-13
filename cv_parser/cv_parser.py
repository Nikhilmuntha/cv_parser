import os
import re
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import zipfile

def extract_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails

def extract_contact_numbers(text):
    pattern = r'(\+\d{1,2}\s?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}'
    contact_numbers = re.findall(pattern, text)
    return ["".join(num) for num in contact_numbers]

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        return process_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return process_docx(file_path)
    else:
        print("Unsupported file format.")
        return ""

def process_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_docx(file_path):
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    text = '\n'.join(paragraphs)
    return text

def create_excel(data):
    df = pd.DataFrame(data, columns=['File', 'Email', 'Contact', 'Text'])
    output_file_path = 'cv_info.xlsx'  # Specify the output file path
    df.to_excel(output_file_path, index=False)
    return output_file_path

def process_cv_bundle(cv_bundle):
    extracted_data = []
    with zipfile.ZipFile(cv_bundle, 'r') as zip_ref:
        extract_dir = 'extracted_cv'  # Specify the directory to extract CV files
        zip_ref.extractall(extract_dir)

        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                text = extract_text(file_path)
                emails = extract_emails(text)
                contact_numbers = extract_contact_numbers(text)
                extracted_data.append({'File': file, 'Email': emails, 'Contact': contact_numbers, 'Text': text})

    output_file_path = create_excel(extracted_data)
    return output_file_path
