
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / "data"
POLICIES_DIR = DATA_DIR / "policies"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Database
DATABASE_PATH = DATA_DIR / "hr_database.db"

# Ollama configuration
OLLAMA_MODEL = "qwen2.5:latest"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text:latest"
OLLAMA_BASE_URL = "http://localhost:11434"

# RAG configuration
CHROMA_COLLECTION_NAME = "hr_policies"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Application
APP_TITLE = "HR Copilot Agent"
APP_VERSION = "1.0.0"
