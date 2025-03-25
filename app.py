import streamlit as st
from bot import process_file, get_llama_response

st.set_page_config(page_title="RAGNexus - Chatbot", layout="wide")

if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #B22222;
            text-align: center;
        }
        .sub-title {
            font-size: 18px;
            text-align: center;
            color: #555;
        }
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
        }
        .chat-box {
            background-color: #ffffff;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .user-msg {
            color: #4169E1;
            font-weight: bold;
            border-left: 4px solid #4169E1;
            padding-left: 10px;
            display: inline-block;
        }
        .ai-msg {
            color: #B22222;
            font-weight: bold;
            border-left: 4px solid #B22222;
            padding-left: 10px;
            display: inline-block;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color: #4169E1;'> Upload Your Document</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader(
    "Upload a file",
    type=["pdf", "docx", "csv", "xlsx", "xls", "png", "jpg", "jpeg", "mp4"],
    help="Supported formats: PDF, DOCX, CSV, Excel (XLSX, XLS), Images (PNG, JPG, JPEG), Videos (MP4)"
)

if uploaded_file:
    with st.spinner("Processing document..."):
        st.session_state.document_text = process_file(uploaded_file)
    st.sidebar.success("Document processed successfully!")

st.markdown("<h1 class='main-title'>RAGNexus - Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Chat with the uploaded document or ask general questions.</p>", unsafe_allow_html=True)

st.subheader("Chat with RAGNexus")
col1, col2 = st.columns([4, 1])

with col1:
    user_query = st.text_input(
        "Ask anything:",
        placeholder="Type your question here...",
        key="chat_input",
        label_visibility="collapsed"
    )
with col2:
    send_pressed = st.button("Send", key="send_chat")

if user_query and (send_pressed or user_query != st.session_state.get("last_query", "")):
    is_doc_query = bool(st.session_state.document_text)
    with st.spinner("Generating response..."):
        answer = get_llama_response(st.session_state.document_text, user_query, is_doc_query)
    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("RAGNexus", answer))
    st.session_state.last_query = user_query

if st.button("Clear Chat", key="clear_chat", help="Click to clear all chat history"):
    st.session_state.chat_history = []
    st.session_state.last_query = ""
    st.success("Chat history cleared.")

st.subheader("Chat History")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, message in st.session_state.chat_history:
    role_class = "user-msg" if role == "You" else "ai-msg"
    st.markdown(f'<div class="chat-box"><span class="{role_class}">{role}:</span> {message}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)