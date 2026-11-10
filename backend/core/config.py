import os
from pathlib import Path


class Settings:
    _defaults = {
        "DATABASE_URL": "sqlite:///./it_troubleshooting.db",
        "GROQ_API_KEY": "",
        "LLM_BASE_URL": "",
        "LLM_API_KEY": "",
        "LLM_MODEL": "gpt-oss-120b",
        "EMBEDDING_MODEL": "BAAI/bge-m3",
        "FAISS_INDEX_PATH": "storage/faiss/index.faiss",
    }

    def __init__(self) -> None:
        dotenv_values = {}
        dotenv_path = Path(".env")
        if dotenv_path.is_file():
            for line in dotenv_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    dotenv_values[key.strip()] = value.strip().strip("\"'")

        for key, default in self._defaults.items():
            setattr(self, key, os.environ.get(key, dotenv_values.get(key, default)))

settings = Settings()
