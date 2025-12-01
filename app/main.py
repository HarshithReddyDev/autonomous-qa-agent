from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_engine import build_knowledge_base, get_retriever
from app.selenium_gen import generate_test_cases, generate_script
import os

app = FastAPI()
ASSETS_DIR = "./assets"

class TestRequest(BaseModel):
    query: str

class ScriptRequest(BaseModel):
    test_case: str

@app.post("/ingest")
def ingest_docs():
    build_knowledge_base(ASSETS_DIR)
    return {"message": "Ingestion Complete"}

@app.post("/generate-tests")
def get_tests(req: TestRequest):
    retriever = get_retriever()
    result = generate_test_cases(retriever, req.query)
    return {"test_cases": result}

@app.post("/generate-script")
def get_script(req: ScriptRequest):
    html_path = os.path.join(ASSETS_DIR, "checkout.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = ""
        
    script = generate_script(req.test_case, html)
    return {"script": script}