from fastapi import FastAPI
from backend.api.routes import documents, chat, tickets
from backend.db.database import Base, engine
from backend import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Troubleshooting Assistant")
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])

@app.get("/")
def home():
    return {"message": "IT Troubleshooting RAG API is running"}
