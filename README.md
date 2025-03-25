# RAGNexus - Document Chat Application

RAGNexus is an interactive chat application that allows users to upload documents and have conversations about their content. The application uses Retrieval-Augmented Generation (RAG) techniques to enable contextual conversations with various document types.

## Features

- **Multi-format Document Support**: Process PDF, DOCX, CSV, Excel, images, and video files
- **Document Context**: Chat with the AI about the content of your uploaded documents
- **General Q&A**: Ask general questions when no document is uploaded
- **Interactive UI**: User-friendly Streamlit interface with styled chat history

## Requirements

- Python 3.8 or higher
- Streamlit
- PyMuPDF
- Pandas
- Python-docx
- Pytesseract
- OpenCV
- Pillow
- Ollama

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install Ollama locally (for the LLM):
   - Follow instructions at [Ollama.ai](https://ollama.ai/) to install
   - Download the llama3.2:3b model:
     ```
     ollama pull llama3.2:3b    ```

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Upload a document using the sidebar uploader.

3. Ask questions about the document in the chat interface.

4. When no document is uploaded, the bot will respond to general questions.

## Project Structure

- `app.py`: Main Streamlit application with the user interface
- `bot.py`: Backend functions for document processing and LLM interaction
- `requirements.txt`: Required Python packages

## How It Works

1. Document Processing:
   - Documents are uploaded and processed based on their type
   - Text is extracted using specialized libraries for each format
   - The extracted text is stored in the session state

2. Question Answering:
   - User questions are sent to the Ollama LLM with the document context
   - The model generates contextual responses based on the uploaded document
   - Without a document, the model answers general questions
