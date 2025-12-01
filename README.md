# 🤖 Autonomous QA Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-v0.3-orange.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.0-yellow.svg)

> **An Agentic RAG system that reads requirements, understands HTML, and autonomously writes self-healing Selenium test scripts.**

---

## 📖 Overview

Traditional test automation is brittle. If a `<div>` ID changes, the script breaks.  
This **Autonomous QA Agent** solves that problem by using **Retrieval Augmented Generation (RAG)** to "read" project documentation and **Vision/Context-Aware LLMs** to generate grounded, robust test scripts.

It separates the **"What to test"** (Logic from Docs) from the **"How to test"** (Selectors from HTML), ensuring 100% traceability.

### 🚀 Key Features
* **🧠 RAG-Driven Intelligence:** Uses **Hybrid Chunking** to parse complex requirements (`.md`, `.txt`) and ground every test case in reality.
* **🕸️ HTML-Grounded Generation:** The agent analyzes the *actual* DOM structure of the target application to select robust IDs and CSS selectors, preventing hallucinations.
* **⚡ Zero-Cost Architecture:** Engineered to run entirely on **Free Tier** resources using **Google Gemini 1.5 Flash** (Logic) and **HuggingFace** (Local Embeddings).
* **🐳 Dockerized & Cloud Ready:** Fully containerized architecture deployable to AWS/GCP Free Tier with swap-memory optimization.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Interactive UI for uploading docs & reviewing tests. |
| **Backend** | **FastAPI** | Async orchestration API handling long-running AI tasks. |
| **Brain (LLM)** | **Gemini 1.5 Flash** | High-speed reasoning & code generation (via LangChain). |
| **Memory** | **ChromaDB** | Vector Store for retrieving relevant requirements. |
| **Embeddings** | **HuggingFace** | `all-MiniLM-L6-v2` running locally on CPU. |
| **Automation** | **Selenium** | Browser automation and validation. |

---

## ⚡ Quick Start

### Option 1: Run with Docker (Recommended)
The easiest way to run the full stack without dependency issues.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/autonomous-qa-agent.git](https://github.com/your-username/autonomous-qa-agent.git)
    cd autonomous-qa-agent
    ```

2.  **Set up secrets:**
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    GROQ_API_KEY=your_groq_key_here (Optional)
    ```

3.  **Launch:**
    ```bash
    docker-compose up --build
    ```
    *Access the UI at [http://localhost:8501](http://localhost:8501)*

### Option 2: Local Python Setup

1.  **Create Virtual Env:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\Activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Services:**
    * **Backend:** `python -m uvicorn app.main:app --reload`
    * **Frontend:** `python -m streamlit run app/ui.py`

---

## 🧪 Usage Workflow

1.  **Ingest Knowledge:**
    * Go to the **"Setup"** sidebar.
    * Click **"Build Knowledge Base"**. The agent ingests `assets/product_specs.md` and `assets/checkout.html`.
2.  **Generate Strategy:**
    * Enter a feature to test (e.g., *"Discount Code Logic"*).
    * The Agent retrieves relevant specs from ChromaDB and generates logical Test Cases (JSON).
3.  **Generate Code:**
    * Select a test case.
    * Click **"Generate Code"**.
    * The Agent reads the `checkout.html` source code to find *real* element IDs and writes a Python Selenium script.

---

## 📂 Repository Structure

```text
├── app/
│   ├── main.py          # FastAPI Endpoints
│   ├── ui.py            # Streamlit Interface
│   ├── rag_engine.py    # ChromaDB & Ingestion
│   └── selenium_gen.py  # LangChain/LLM Logic
├── assets/              # Test Targets (HTML/Docs)
├── Dockerfile           # Deployment Config
└── requirements.txt     # Dependencies