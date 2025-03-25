import ollama
import fitz
import pandas as pd
import pytesseract
import cv2
import os
from PIL import Image
from docx import Document
import streamlit as st
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "\n".join([page.get_text("text") for page in doc])
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])
def extract_text_from_csv(csv_file):
    try:
        try:
            df = pd.read_csv(csv_file)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, encoding='latin1')
        if df.empty:
            return "The CSV file is empty."
        text = "CSV File Analysis:\n\n"
        text += f"Dataset Overview:\n"
        text += f"- Total Records: {len(df)}\n"
        text += f"- Total Features: {len(df.columns)}\n"
        text += f"- Columns: {', '.join(df.columns)}\n\n"
        text += "Sample Data (First 5 rows):\n"
        text += df.head().to_string() + "\n\n"
        return text
    except pd.errors.EmptyDataError:
        return "The CSV file appears to be empty or invalid."
    except Exception as e:
        return f"Error processing CSV file: {str(e)}"
def extract_text_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file)
        text = "Excel File Analysis:\n\n"
        text += f"Dataset Overview:\n"
        text += f"- Total Records: {len(df)}\n"
        text += f"- Total Features: {len(df.columns)}\n"
        text += f"- Columns: {', '.join(df.columns)}\n\n"
        text += "Sample Data (First 5 rows):\n"
        text += df.head().to_string() + "\n\n"
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            text += "Statistical Summary:\n"
            for col in numeric_cols:
                text += f"\n{col}:\n"
                text += f"  Mean: {df[col].mean():.2f}\n"
                text += f"  Median: {df[col].median():.2f}\n"
                text += f"  Min: {df[col].min()}\n"
                text += f"  Max: {df[col].max()}\n"
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            text += "\nCategorical Columns:\n"
            for col in cat_cols:
                unique_vals = df[col].nunique()
                text += f"\n{col}:\n"
                text += f"  - Unique Values: {unique_vals}\n"
                if unique_vals < 10:  # Only show value counts for columns with few unique values
                    text += f"  - Value Counts:\n"
                    for val, count in df[col].value_counts().items():
                        text += f"    {val}: {count}\n"
        return text
    except Exception as e:
        return f"Error processing Excel file: {str(e)}"
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)
def extract_text_from_video(video_file):
    temp_video_path = "temp_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(video_file.getbuffer())
    cap = cv2.VideoCapture(temp_video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    interval = fps * 5
    frame_count = 0
    text = ""
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            text += pytesseract.image_to_string(image) + "\n"
        frame_count += 1
    cap.release()
    os.remove(temp_video_path)
    return text.strip()
def process_file(uploaded_file):
    file_type = uploaded_file.type
    text = ""
    if "pdf" in file_type:
        text = extract_text_from_pdf(uploaded_file)
    elif "word" in file_type or "msword" in file_type:
        text = extract_text_from_docx(uploaded_file)
    elif "csv" in file_type:
        text = extract_text_from_csv(uploaded_file)
    elif "spreadsheet" in file_type or "excel" in file_type:  # For Excel
        text = extract_text_from_excel(uploaded_file)
    elif "image" in file_type:
        text = extract_text_from_image(uploaded_file)
    elif "video" in file_type:
        text = extract_text_from_video(uploaded_file)
    return text.strip()
def get_llama_response(context, query, is_doc_query):
    if is_doc_query:
        prompt = f"""
        You are an AI assistant. Answer the user's question based on the provided document content.
        Document Content: {context}
        User Question: {query}
        Answer:
        """
    else:
        prompt = query
    try:
        response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"Error generating response: {str(e)}"
