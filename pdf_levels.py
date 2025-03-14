import pdfplumber
from transformers import pipeline
# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Function to summarize text
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # TODO adjust parameters based on sample text.
    summary = summarizer(text, max_length=400, min_length=200, do_sample=False)
    return summary[0]['summary_text']


# Answer questions
def answer_question(text, question):
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    result = qa_pipeline(question=question, context=text)
    return result['answer']

# Generate explanation at different expertise levels
def explain_answer(text, answer, level="beginner"):
    generator = pipeline("text2text-generation", model="google/flan-t5-large")
    if level == "beginner":
        prompt = f"Explain '{answer}' from this text in simple terms for a beginner: {text}"
    elif level == "intermediate":
        # prompt = f"Explain '{answer}' from this text with moderate detail: {text}"
        prompt = f"Convert this summary into a vivid image generation prompt: {text}"
    else:  # expert
        prompt = f"Provide a detailed, technical explanation of '{answer}' from this text: {text}"
    explanation = generator(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']
    return explanation


# Example usage
pdf_path = "pdfs/goods-flow-management.pdf"
pdf_text = extract_text_from_pdf(pdf_path)
summary = summarize_text(pdf_text)
print("Summary:", summary)

# Example usage
question = "What are the steps of cargo reception?"

# Get the answer
# answer = answer_question(pdf_text, question)
# print("Answer:", answer)

# Get explanations at different levels
beginner_explanation = explain_answer(pdf_text, summary, "beginner")
intermediate_explanation = explain_answer(pdf_text, summary, "intermediate")
expert_explanation = explain_answer(pdf_text, summary, "expert")

print("Beginner Explanation:", beginner_explanation)
print("Intermediate Explanation:", intermediate_explanation)
print("Expert Explanation:", expert_explanation)
