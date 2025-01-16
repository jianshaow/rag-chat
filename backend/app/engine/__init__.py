import os
from dotenv import load_dotenv

load_dotenv()

data_base_dir = os.getenv("DATA_BASE_DIR", "data")
uploaded_data_dir = os.getenv("UPLOADED_DATA_DIR", "uploaded")
chroma_base_dir = os.getenv("CHROMA_BASE_DIR", "chroma")
model_provider = os.getenv("MODEL_PROVIDER", "ollama")

ollama_host = os.getenv("OLLAMA_HOST", "localhost")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", f"http://{ollama_host}:11434")
ollama_embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text:v1.5")
ollama_chat_model = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:14b")

openai_embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")
openai_chat_model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

gemini_embed_model = os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001")
gemini_chat_model = os.getenv("GEMINI_CHAT_MODEL", "models/gemini-1.5-flash")
