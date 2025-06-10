import os
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader

# Load environment variables from .env file
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file.
    """
    if not os.path.exists(pdf_path):
        if os.path.exists(os.path.join("..", pdf_path)):
            pdf_path = os.path.join("..", pdf_path)
        else:
            raise FileNotFoundError(f"PDF file not found at expected path: {pdf_path}")
    
    print(f"Extracting text from PDF: {pdf_path}")
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n\n"
    
    return text

def save_processed_text(text, pdf_path):
    """
    Save processed text to a file.
    """
    output_dir = os.path.join(os.path.dirname(pdf_path), "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_processed.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Processed text saved to: {output_file}")
    return output_file

def bootstrap_assistant():
    """
    Process PDF and prepare it for Q&A.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    pdf_path = os.getenv("PDF_PATH", os.path.join("../data", "lecture-1.pdf"))

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Save processed text
    processed_file = save_processed_text(text, pdf_path)
    
    print("\nBootstrap process completed.")
    print("Your text has been processed and is ready for Q&A.")
    print(f"Processed file location: {processed_file}")

if __name__ == "__main__":
    bootstrap_assistant()