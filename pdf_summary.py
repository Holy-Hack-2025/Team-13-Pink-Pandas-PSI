# Install required packages
# pip install pdfplumber transformers torch

import pdfplumber
from transformers import pipeline

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to summarize text
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # TODO adjust parameters based on sample text.
    summary = summarizer(text, max_length=400, min_length=200, do_sample=False)
    return summary[0]['summary_text']

# Example usage
pdf_path = "pdfs/goods-flow-management.pdf"
pdf_text = extract_text_from_pdf(pdf_path)
summary = summarize_text(pdf_text)
print("Summary:", summary)