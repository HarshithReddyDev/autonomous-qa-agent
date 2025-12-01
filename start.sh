#!/bin/bash

# Start FastAPI in the background (&)
# --host 0.0.0.0 is required for Docker networking
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit in the foreground
streamlit run app/ui.py --server.port 8501 --server.address 0.0.0.0