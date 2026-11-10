from sentence_transformers import SentenceTransformer
from backend.core.config import settings

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def embed_texts(texts):
    return get_model().encode(texts, normalize_embeddings=True, convert_to_numpy=True)

def embed_query(text):
    return embed_texts([text])
