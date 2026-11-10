# IT Troubleshooting RAG

## Setup

1. Create a PostgreSQL database named `it_troubleshooting`.
2. Create an environment: `python -m venv .venv`
3. Activate it and install: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set database and LLM credentials.
5. Start the API: `uvicorn backend.main:app --reload`
6. Start Streamlit in another terminal: `streamlit run frontend/app.py`

The first embedding run downloads BAAI/bge-m3 and may take time. The LLM endpoint must expose an OpenAI-compatible `/chat/completions` route.

## API

- `POST /documents/upload` multipart file
- `GET /documents`
- `DELETE /documents/{document_id}`
- `POST /chat` JSON: `{"question":"...","ticket_id":"optional-ticket-id"}`
- `GET /tickets/{ticket_id}/messages`

TXT and PDF uploads are supported. The initial local knowledge base can be ingested with `python -m backend.seed`.

FAISS and BM25 indexes are rebuilt from active chunks after document changes. PostgreSQL stores document/chunk metadata and ticket history. This is a practical MVP; production deployments should add authentication, background jobs, migrations, robust PDF layout extraction, and index versioning.
