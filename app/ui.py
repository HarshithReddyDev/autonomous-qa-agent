import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="OceanAI Agent", layout="wide")

st.title("🤖 Autonomous QA Agent")
st.markdown("Powered by **Groq Llama 3** (Free Cloud) & **HuggingFace** (Local Embeddings)")

# --- Sidebar: Knowledge Base Setup ---
with st.sidebar:
    st.header("1. Setup")
    st.info("Make sure your backend is running!")
    
    if st.button("Build Knowledge Base"):
        with st.spinner("Ingesting docs & creating embeddings..."):
            try:
                # Calls the /ingest endpoint in FastAPI
                response = requests.post(f"{API_URL}/ingest")
                if response.status_code == 200:
                    st.success("✅ Knowledge Base Built Successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
                st.warning("Did you run 'python -m uvicorn app.main:app --reload'?")

# --- Main Layout ---
col1, col2 = st.columns(2)

# --- Column 1: Test Case Generation ---
with col1:
    st.subheader("2. Test Case Generation")
    feature = st.text_input("Feature to Test", "Discount Code Logic")
    
    if st.button("Generate Test Cases"):
        with st.spinner("Thinking (RAG + Llama 3)..."):
            try:
                payload = {"query": feature}
                res = requests.post(f"{API_URL}/generate-tests", json=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    st.session_state['tests'] = data['test_cases']
                    st.success("Test Cases Generated!")
                else:
                    st.error(f"Backend Error: {res.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
    
    # Display Generated JSON if available
    if 'tests' in st.session_state:
        st.text_area("Generated JSON", st.session_state['tests'], height=300)

# --- Column 2: Selenium Code Generation ---
with col2:
    st.subheader("3. Selenium Script")
    
    # User can edit the JSON before generating code
    selected_case = st.text_area("Paste One Test Case JSON Here", height=150, 
                                 placeholder='{"id": "TC01", "description": "..."}')
    
    if st.button("Generate Code"):
        if selected_case:
            with st.spinner("Writing Selenium Code..."):
                try:
                    payload = {"test_case": selected_case}
                    res = requests.post(f"{API_URL}/generate-script", json=payload)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state['code'] = data['script']
                        st.success("Code Generated!")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please paste a test case first.")
    
    # Display Generated Python Code
    if 'code' in st.session_state:
        st.code(st.session_state['code'], language="python")