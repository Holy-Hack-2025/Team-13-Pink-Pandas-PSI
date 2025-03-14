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
    # Get the tokenizer from the summarizer
    tokenizer = summarizer.tokenizer
    # Tokenize the text to get the actual input length in tokens
    tokens = tokenizer(text, truncation=True, max_length=1024, return_tensors="pt")
    input_length = tokens["input_ids"].shape[1]  # Number of tokens
    print(f"Tokenized input length: {input_length}")
    
    # Set max_length and min_length based on token count
    max_length = input_length // 2  # Half the input length
    min_length = input_length // 4  # Quarter the input length
    
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

# Example usage
datadir = "pdfs"
file = "goods-flow-management"
pdf_path = f"{datadir}/{file}.pdf"
pdf_text = extract_text_from_pdf(pdf_path)
lentxt = len(pdf_text)
print("Length of the pdf", lentxt)
summary = summarize_text(pdf_text)
print("Summary:", summary)

with open(f"output/summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)