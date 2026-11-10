from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.models import Document
from backend.schemas.document import DocumentOut
from backend.services.document_service import ingest_path, delete_document, UPLOAD_DIR
from backend.utils.file_validation import validate_upload

router = APIRouter()

@router.post("/upload", response_model=DocumentOut)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        validate_upload(file.filename)
        destination = UPLOAD_DIR / f"{Path(file.filename).stem}_{Path(file.filename).suffix.lstrip('.')}"
        destination.write_bytes(file.file.read())
        return ingest_path(db, destination, file.filename)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.status == "active").all()

@router.delete("/{document_id}")
def remove_document(document_id: int, db: Session = Depends(get_db)):
    if not delete_document(db, document_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted"}
