import streamlit as st
from core.pdf_processor import process_pdf
import tempfile

st.set_page_config(page_title="PDF Reorder Tool", layout="wide")

st.title("📄 Jumbled PDF Reorder Tool")
st.write("Upload a jumbled multi-page PDF, and we'll attempt to reorder it intelligently.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    st.info("Processing your PDF...")
    output_pdf, reasoning = process_pdf(tmp_path)
    
    if output_pdf:
        st.success("PDF Reordered Successfully!")
        with open(output_pdf, "rb") as f:
            st.download_button("⬇ Download Reordered PDF", f, file_name="reordered.pdf")
        
        st.subheader("📑 Reordering Reasoning")
        st.write(reasoning)
    else:
        st.error("Could not process PDF. Please check the file format.")
