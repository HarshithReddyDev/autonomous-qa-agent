import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Load Environment Variables (API Keys)
load_dotenv()

# 2. Initialize Groq (The "Brain")
# Using Llama 3.3 which is currently active and free on Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_retries=2
)

def generate_test_cases(retriever, query):
    """
    Phase 2: Generate logical test cases from the documentation (RAG).
    """
    # Retrieve relevant docs from Vector DB based on the user's query
    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])
    
    template = """
    You are a generic QA Lead.
    Based ONLY on the provided Context, generate 3 comprehensive test cases for the feature: "{query}".
    
    CONTEXT from Documentation:
    {context}
    
    OUTPUT FORMAT:
    Return a raw JSON list. Do NOT use markdown code blocks.
    [
        {{
            "id": "TC01",
            "description": "...",
            "steps": "1. Step one, 2. Step two...",
            "expected_result": "..."
        }}
    ]
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    # Invoke the chain and clean up the response to ensure valid JSON
    response = chain.invoke({"context": context, "query": query})
    return response.content.replace("```json", "").replace("```", "").strip()

def generate_script(test_case_str, html_content):
    """
    Phase 3: Generate executable Selenium Python code.
    """
    template = """
    You are a Senior SDET (Software Development Engineer in Test). 
    Write a production-ready Python Selenium script for this test case.
    
    TEST CASE:
    {test_case}
    
    TARGET HTML (Source of Truth):
    {html_content}
    
    RULES:
    1. Use 'webdriver.Chrome()'
    2. LOOK at the HTML provided. Use the EXACT IDs found in the HTML (e.g. if id="discount-code", use By.ID, "discount-code").
    3. If an ID is missing, use a robust CSS selector.
    4. Add 'import' statements (selenium, webdriver, By, WebDriverWait, etc.).
    5. Return ONLY the python code. No markdown formatting.
    6. IMPORTANT: Assume the user is running this locally. Do NOT use headless mode yet.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    response = chain.invoke({"test_case": test_case_str, "html_content": html_content})
    return response.content.replace("```python", "").replace("```", "").strip()