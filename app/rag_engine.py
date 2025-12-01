import os
from langchain_community.document_loaders import TextLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# ⬇️ CHANGED: Import from the new dedicated package
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "./chroma_db"

def build_knowledge_base(assets_path):
    docs = []
    
    md_path = os.path.join(assets_path, "product_specs.md")
    if os.path.exists(md_path):
        print(f"Loading {md_path}...")
        docs.extend(TextLoader(md_path, encoding='utf-8').load())
        
    html_path = os.path.join(assets_path, "checkout.html")
    if os.path.exists(html_path):
        print(f"Loading {html_path}...")
        docs.extend(BSHTMLLoader(html_path, encoding='utf-8').load())

    if not docs:
        print("No documents found to ingest!")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(docs)
    
    print("Embedding documents (this runs locally)...")
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # ⬇️ CHANGED: Chroma initialization for new version
    Chroma.from_documents(
        documents=splits, 
        embedding=embedding_function, 
        persist_directory=DB_PATH
    )
    print(f"Knowledge Base built with {len(splits)} chunks.")

def get_retriever():
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory=DB_PATH, embedding_function=embedding_function).as_retriever()