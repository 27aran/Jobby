from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# Projekt-Root: von src/jobby/config.py zwei Ebenen hoch
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    claude_model: str
    embedding_model: str
    db_path: Path
    qdrant_path: Path
    profile_dir: Path


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} fehlt in .env")
    return value


settings = Settings(
    anthropic_api_key=_require("ANTHROPIC_API_KEY"),
    claude_model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"),
    embedding_model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"),
    db_path=ROOT / os.getenv("DB_PATH", "data/jobby.db"),
    qdrant_path=ROOT / os.getenv("QDRANT_PATH", "data/qdrant"),
    profile_dir=ROOT / os.getenv("PROFILE_DIR", "profile"),
)