# AI-Powered Study Assistant

This project is an AI-powered study assistant that helps you process PDF lecture materials, generate study notes, and answer questions about the content.

## Features

- PDF text extraction and processing
- AI-powered Q&A system for asking questions about the content
- Automatic note generation in both Markdown and JSON formats
- Interactive command-line interface

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Process a PDF file:
```bash
python scripts/00_bootstrap.py
```

2. Ask questions about the content:
```bash
python scripts/01_qna_assistant.py
```

3. Generate study notes:
```bash
python scripts/02_generate_notes.py
```

## Project Structure

```
.
├── data/
│   ├── processed/    # Processed text files
│   └── notes/        # Generated notes
├── scripts/
│   ├── 00_bootstrap.py      # PDF processing script
│   ├── 01_qna_assistant.py  # Q&A system
│   └── 02_generate_notes.py # Notes generator
├── .env              # Environment variables
├── .gitignore       # Git ignore file
├── README.md        # This file
└── requirements.txt # Project dependencies
```

## Requirements

- Python 3.8+
- OpenAI API key
- Required Python packages (see requirements.txt)
