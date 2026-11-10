from pathlib import Path
from backend.db.database import Base, engine, SessionLocal
from backend import models
from backend.services.document_service import ingest_path

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    folder = Path("data/knowledge_base/raw")
    for path in sorted(folder.glob("*.txt")):
        try:
            ingest_path(db, path, path.name)
            print(f"Indexed {path.name}")
        except Exception as error:
            print(f"Skipped {path.name}: {error}")
finally:
    db.close()
