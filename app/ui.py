import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="OceanAI Agent", layout="wide")
st.title("🤖 Autonomous QA Agent")
st.markdown("Powered by **Gemini 1.5 Flash** (Free) & **HuggingFace** (Local)")

# Sidebar
with st.sidebar:
    st.header("1. Setup")
    if st.button("Build Knowledge Base"):
        with st.spinner("Ingesting & Vectorizing..."):
            try:
                requests.post(f"{API_URL}/ingest")
                st.success("✅ Knowledge Base Ready!")
            except:
                st.error("Is the backend running?")

# Main Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("2. Test Case Generation")
    feature = st.text_input("Feature to Test", "Discount Code Logic")
    
    if st.button("Generate Test Cases"):
        with st.spinner("Thinking..."):
            res = requests.post(f"{API_URL}/generate-tests", json={"query": feature})
            st.session_state['tests'] = res.json()['test_cases']
    
    if 'tests' in st.session_state:
        st.text_area("Generated JSON", st.session_state['tests'], height=300)

with col2:
    st.subheader("3. Selenium Script")
    # Allow user to edit/select a specific case
    selected_case = st.text_area("Paste One Test Case Here", height=150)
    
    if st.button("Generate Code"):
        if selected_case:
            with st.spinner("Coding..."):
                res = requests.post(f"{API_URL}/generate-script", json={"test_case": selected_case})
                st.session_state['code'] = res.json()['script']
    
    if 'code' in st.session_state:
        st.code(st.session_state['code'], language="python")