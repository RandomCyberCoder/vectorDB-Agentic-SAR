from PyPDF2 import PdfReader
import PyPDF2
import os
import json
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from chunking.clean_text import clean_text
from langchain_text_splitters import NLTKTextSplitter

load_dotenv()

PDF_FILE_PATH = os.getenv("PDF_FILE_PATH", "chunking/data/Chunking.pdf")
PDF_PASSWORD = os.getenv("PDF_PASSWORD", "")
outfile = "chunking/data/extracted/extracted_pages.json"


provenance = {"source": "Intelligent Search Managing the Intelligence Process in the Search for Missing Persons",
                            "author": "Christopher S. Young"}

def read_password_protected_pdf(pdf_path, password):    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode("Requiring information on how to locate missing people and steps that can"
    "be taken to finding missing people", convert_to_tensor=True)

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
        passages = []
        last_page = float('-inf')
        for i, page in enumerate(reader.pages):
            if i + 1 in page_skip_list:
                continue

            page_text = clean_text(page.extract_text() or "")
            page_embedding = model.encode(page_text, convert_to_tensor=True)
            cosine_score = util.cos_sim(query_embedding, page_embedding).item()
            if cosine_score < 0.3:
                continue

            print(f"Page {i + 1} cosine similarity score: {cosine_score:.4f}")
            if i - 1 == last_page:
                passages[-1] += "\n" + page_text
                continue

            else:
                passages.append(page_text)
            last_page = i
        return passages


def chunk_passages(passages):
    text_splitter = NLTKTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    all_chunks = []
    for passage in passages:
        chunks = text_splitter.split_text(passage)
        all_chunks.extend(chunks)
    return all_chunks

def format_chunks(chunks):
    formated = []
    for chunk in chunks:
        formated.append({
            "provenance": provenance,
            "content": chunk
        })
    return formated

def main():
    pdf_chunks = read_password_protected_pdf(PDF_FILE_PATH, PDF_PASSWORD)
    if not pdf_chunks:
        print("No text extracted from PDF.")
        return
    
    chunks = chunk_passages(pdf_chunks)
    formatted_chunks = format_chunks(chunks)
    
    with open(outfile, "w") as f:
        json.dump(formatted_chunks, f, indent=4)
        
if __name__ == "__main__":
    main()