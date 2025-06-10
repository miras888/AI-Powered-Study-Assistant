import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

class QnAAssistant:
    def __init__(self):
        """
        Initialize the Q&A assistant.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        self.context = self.load_processed_content()
    
    def load_processed_content(self):
        """
        Load the processed PDF content.
        """
        processed_dir = "../data/processed"
        if not os.path.exists(processed_dir):
            print("Warning: No processed content found")
            return ""
            
        # Find the most recent processed file
        processed_files = [f for f in os.listdir(processed_dir) if f.endswith("_processed.txt")]
        if not processed_files:
            print("Warning: No processed files found")
            return ""
            
        latest_file = max(processed_files, key=lambda x: os.path.getctime(os.path.join(processed_dir, x)))
        file_path = os.path.join(processed_dir, latest_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading processed content: {e}")
            return ""
    
    def ask_question(self, question):
        """
        Ask a question and get a response.
        """
        if not self.context:
            return "Error: No content has been processed yet. Please run the bootstrap script first."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful tutor. Answer questions based on the provided context."},
                    {"role": "user", "content": f"Context:\n{self.context}\n\nQuestion: {question}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response: {e}"

def main():
    # Create the assistant
    assistant = QnAAssistant()
    
    # Interactive Q&A loop
    print("\nWelcome to the Q&A Assistant!")
    print("Type 'exit' to quit")
    print("Type 'reload' to reload the processed content")
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() == 'exit':
            break
        elif question.lower() == 'reload':
            assistant.context = assistant.load_processed_content()
            print("Content reloaded!")
            continue
            
        if not question:
            continue
            
        print("\nAssistant's response:")
        answer = assistant.ask_question(question)
        print(answer)

if __name__ == "__main__":
    main()