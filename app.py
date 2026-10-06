import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
# -----------------------------------------
# Load API key
# -----------------------------------------
load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")
# -----------------------------------------
# Page setup
# -----------------------------------------
st.set_page_config(
    page_title="AI Student Data Assistant",
    page_icon="🎓",
    layout="wide"
)
st.title("🎓 AI Student Data Assistant")
st.write("Upload a student PDF containing marks and attendance, then ask questions about it.")
# -----------------------------------------
# Check API key
# -----------------------------------------
if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()
# -----------------------------------------
# Gemini client
# -----------------------------------------
client = genai.Client(api_key=api_key)
# -----------------------------------------
# Upload PDF
# -----------------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Student PDF",
    type=["pdf"]
)
if uploaded_file is not None:
    try:
        # -----------------------------------------
        # Read PDF
        # -----------------------------------------
        reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"
        # -----------------------------------------
        # Check extracted text
        # -----------------------------------------
        if not pdf_text.strip():
            st.error(
                "Could not extract text from this PDF. "
                "Please upload a text-based PDF."
            )
            st.stop()
        st.success("✅ Student PDF uploaded successfully!")
        # -----------------------------------------
        # Show extracted information
        # -----------------------------------------
        st.subheader("📄 Extracted Student Data")
        with st.expander("View PDF text"):
            st.text(pdf_text)
        # -----------------------------------------
        # Ask AI
        # -----------------------------------------
        st.subheader("🤖 Ask AI About Student Data")
        question = st.text_input(
            "Enter your question:",
            placeholder="Example: What is the overall attendance?"
        )
        if st.button("🔎 Analyze"):
            if not question.strip():
                st.warning("Please enter a question.")
                st.stop()
            # -----------------------------------------
            # Prompt
            # -----------------------------------------
            prompt = f"""
You are an AI Student Data Assistant.
Use only the information available in the student PDF text below.
STUDENT PDF DATA:
{pdf_text}
USER QUESTION:
{question}
Instructions:
- Answer clearly and simply.
- Do not invent information.
- Use the exact values available in the PDF.
- If the answer is not available in the PDF, say:
  "This information is not available in the uploaded PDF."
"""
            # -----------------------------------------
            # Gemini
            # -----------------------------------------
            with st.spinner("🤖 AI is analyzing the student PDF..."):

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
            # -----------------------------------------
            # Display answer
            # -----------------------------------------
            st.subheader("💡 AI Answer")
            if response and response.text:
                st.write(response.text)
            else:
                st.warning("No answer received from Gemini.")
    except Exception as e:
        st.error(f"Error while reading PDF: {e}")
else:
    st.info("👆 Upload a student PDF to start.")