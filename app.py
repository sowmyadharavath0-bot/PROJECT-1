import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
# Load environment variables
load_dotenv()
# Gemini API
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
# Page configuration
st.set_page_config(
    page_title="AI Data Analysis Assistant",
    page_icon="📊",
    layout="wide"
)
st.title("📊 AI Data Analysis Assistant")
st.write("Upload a CSV file and ask questions about your data.")
# Upload CSV
uploaded_file = st.file_uploader(
    "Upload your subject pdf file",
    type=["pdf"]
)
if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(
        uploaded_file,
        encoding="latin1",
        engine="python",
        on_bad_lines="skip"
    )
    st.success("CSV file uploaded successfully!")
    # Dataset preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(10))
    # Dataset information
    st.subheader("📊 Dataset Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))
    # Basic statistics
    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe(include="all"))
    # Column information
    st.subheader("🔍 Columns")
    st.write(list(df.columns))
    # User question
    st.subheader("🤖 Ask AI")
    question = st.text_input(
        "Ask something about your dataset:"
    )
    if st.button("Analyze"):
        if question:
            # Convert sample data to text
            sample_data = df.head(20).to_string()
            prompt = f"""
You are an AI Data Analysis Assistant.
Analyze the following dataset and answer the user's question.
Dataset columns:
{list(df.columns)}
Dataset shape:
{df.shape}
Sample data:
{sample_data}
Basic statistics:
{df.describe(include="all").to_string()}
User question:
{question}
Give a clear and simple answer.
If calculations are required, explain the result.
"""
            with st.spinner("AI is analyzing the data..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
            st.subheader("🤖 AI Answer")
            st.write(response.text)
        else:
            st.warning("Please enter a question.")