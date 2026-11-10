from pathlib import Path
import faiss
import numpy as np
from backend.core.config import settings
from backend.services.retrieval.embedding_service import embed_texts, embed_query

class FaissStore:
    def __init__(self):
        self.index = None
        self.items = []

    def build(self, items):
        self.items = items
        if not items:
            self.index = None
            return
        vectors = embed_texts([item["content"] for item in items]).astype("float32")
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

    def search(self, query, k=8):
        if self.index is None:
            return []
        scores, indices = self.index.search(embed_query(query).astype("float32"), min(k, len(self.items)))
        return [dict(self.items[i], score=float(score), rank=rank + 1) for rank, (i, score) in enumerate(zip(indices[0], scores[0])) if i >= 0]

    def save(self):
        if self.index is not None:
            path = Path(settings.FAISS_INDEX_PATH)
            path.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(path))
