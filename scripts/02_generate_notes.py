import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

class NotesGenerator:
    def __init__(self):
        """
        Initialize the Notes Generator.
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
    
    def generate_notes(self, format_type="markdown"):
        """
        Generate structured notes from the content.
        
        Args:
            format_type (str): The format of the notes ('markdown' or 'json')
        """
        if not self.context:
            return "Error: No content has been processed yet. Please run the bootstrap script first."
        
        try:
            # First, get a structured outline
            outline_prompt = """Create a detailed outline of the following content. 
            Break it down into main topics, subtopics, and key points.
            Format the response as a JSON object with the following structure:
            {
                "title": "Main title of the content",
                "sections": [
                    {
                        "title": "Section title",
                        "subsections": [
                            {
                                "title": "Subsection title",
                                "key_points": ["point 1", "point 2", ...]
                            }
                        ]
                    }
                ]
            }"""
            
            outline_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional note-taker and educator."},
                    {"role": "user", "content": f"{outline_prompt}\n\nContent:\n{self.context}"}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            outline = json.loads(outline_response.choices[0].message.content)
            
            if format_type == "json":
                return outline
            
            # Generate detailed notes in markdown format
            notes_prompt = f"""Based on the following outline, create detailed study notes in markdown format.
            Include:
            1. Clear headings and subheadings
            2. Bullet points for key concepts
            3. Important definitions and explanations
            4. Examples where relevant
            5. Key takeaways
            
            Outline:
            {json.dumps(outline, indent=2)}
            
            Content for reference:
            {self.context}"""
            
            notes_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional note-taker and educator."},
                    {"role": "user", "content": notes_prompt}
                ],
                temperature=0.7
            )
            
            return notes_response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating notes: {e}"
    
    def save_notes(self, notes, format_type="markdown"):
        """
        Save the generated notes to a file.
        """
        if not notes:
            return "Error: No notes to save."
            
        # Create notes directory if it doesn't exist
        notes_dir = "../data/notes"
        os.makedirs(notes_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = "md" if format_type == "markdown" else "json"
        filename = f"notes_{timestamp}.{extension}"
        filepath = os.path.join(notes_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if format_type == "json":
                    json.dump(notes, f, indent=2)
                else:
                    f.write(notes)
            return f"Notes saved successfully to {filepath}"
        except Exception as e:
            return f"Error saving notes: {e}"

def main():
    # Create the notes generator
    generator = NotesGenerator()
    
    print("\nWelcome to the Notes Generator!")
    print("1. Generate Markdown Notes")
    print("2. Generate JSON Notes")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            notes = generator.generate_notes(format_type="markdown")
            print("\nGenerated Notes:")
            print("="*50)
            print(notes)
            print("="*50)
            result = generator.save_notes(notes, format_type="markdown")
            print(result)
            
        elif choice == "2":
            notes = generator.generate_notes(format_type="json")
            print("\nGenerated Notes Structure:")
            print("="*50)
            print(json.dumps(notes, indent=2))
            print("="*50)
            result = generator.save_notes(notes, format_type="json")
            print(result)
            
        elif choice == "3":
            print("Exiting Notes Generator. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 
