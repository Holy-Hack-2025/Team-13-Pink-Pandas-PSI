# Install required packages
# pip install pdfplumber transformers torch

import pdfplumber
from transformers import pipeline
import argparse
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""  # Handle None values
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

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Summarize a PDF and save the summary as a text file.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file (e.g., pdfs/goods-flow-management.pdf)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(args.pdf_path)
    lentxt = len(pdf_text)
    print("Length of the pdf (characters):", lentxt)
    
    # Summarize the text
    summary = summarize_text(pdf_text)
    print("Summary:", summary)
    
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Derive output filename from the PDF filename
    pdf_filename = os.path.basename(args.pdf_path).replace(".pdf", "")  # e.g., "goods-flow-management"
    output_file = os.path.join(output_dir, f"summary.txt")
    
    # Save the summary
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(summary)
    print(f"Summary saved to {output_file}")