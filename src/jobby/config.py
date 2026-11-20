from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# Projekt-Root: von src/jobby/config.py zwei Ebenen hoch
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

ALLOWED_PROVIDERS = {"gemini", "anthropic", "ollama", "openrouter"}


@dataclass(frozen=True)
class Settings:
    # LLM
    llm_provider: str
    llm_model: str | None
    gemini_api_key: str | None
    openrouter_api_key: str | None
    anthropic_api_key: str | None
    ollama_api_key: str | None

    # Embeddings
    embedding_model: str

    # Pfade
    db_path: Path
    qdrant_path: Path
    profile_dir: Path


def _load_provider() -> str:
    provider = os.getenv("LLM_PROVIDER", "openrouter").strip().lower()
    if provider not in ALLOWED_PROVIDERS:
        raise RuntimeError(
            f"Unbekannter LLM_PROVIDER '{provider}'. "
            f"Erlaubt: {', '.join(sorted(ALLOWED_PROVIDERS))}"
        )
    return provider


settings = Settings(
    llm_provider=_load_provider(),
    llm_model=os.getenv("LLM_MODEL") or None,
    gemini_api_key=os.getenv("GEMINI_API_KEY") or None,
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY") or None,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or None,
    ollama_api_key=os.getenv("OLLAMA_API_KEY") or None,
    embedding_model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"),
    db_path=ROOT / os.getenv("DB_PATH", "data/jobby.db"),
    qdrant_path=ROOT / os.getenv("QDRANT_PATH", "data/qdrant"),
    profile_dir=ROOT / os.getenv("PROFILE_DIR", "profile"),
)