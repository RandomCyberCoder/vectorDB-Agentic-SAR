from PyPDF2 import PdfReader
import PyPDF2
import os
import json
from dotenv import load_dotenv

load_dotenv()

PDF_FILE_PATH = os.getenv("PDF_FILE_PATH", "chunking/data/Chunking.pdf")
PDF_PASSWORD = os.getenv("PDF_PASSWORD", "")
outfile = "chunking/data/extracted/extracted_pages.json"



def read_password_protected_pdf(pdf_path, password):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return None
    
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except Exception as e:
                print("Failed to decrypt PDF:", e)
                return None
        page_skip_ranges = [(1, 27), (41, 41), (43, 43), (66, 67), (73, 73), (104, 105),
                      (117, 117), (145, 147), (163, 163), (177, 177), (187, 187), (213, 213),
                      (229, 229), (233, 233), (262, 286), (297, 309)]
        page_skip_list = [i for start, end in page_skip_ranges for i in range(start, end + 1)]
        pages = []
        for i, page in enumerate(reader.pages):
            if i + 1 in page_skip_list:
                continue
            provenance = {"source": "Intelligent Search Managing the Intelligence Process in the Search for Missing Persons", 
                          "page": i + 1, 
                          "author": "Christopher S. Young"}
            page_info = {
                "provenance": provenance,
                "content": page.extract_text() or "",
            }
            pages.append(page_info)
        return pages

def main():
    pdf_pages = read_password_protected_pdf(PDF_FILE_PATH, PDF_PASSWORD)
    if pdf_pages:
        print(f"Extracted pages written to : {outfile}")
        print(f"Total pages extracted: {len(pdf_pages)}")
        with open(outfile, "w") as f:
            json.dump(pdf_pages, f, indent=4)
    else:
        print("No text extracted.")

if __name__ == "__main__":
    main()