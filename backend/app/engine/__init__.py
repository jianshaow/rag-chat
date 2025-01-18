"""Environments here."""

import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
DATA_BASE_DIR = os.getenv("DATA_BASE_DIR", "data")
DATA_DIR = os.getenv("DATA_DIR", "en_novel")

UPLOADED_DATA_DIR = os.getenv("UPLOADED_DATA_DIR", "uploaded")
CHROMA_BASE_DIR = os.getenv("CHROMA_BASE_DIR", "chroma")
STORAGE_BASE_DIR = os.getenv("STORAGE_BASE_DIR", "storage")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", f"http://{OLLAMA_HOST}:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text:v1.5")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:14b")

OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001")
GEMINI_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "models/gemini-1.5-flash")
