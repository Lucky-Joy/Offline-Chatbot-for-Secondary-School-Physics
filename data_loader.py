import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
KB_PATH = DATA_DIR / "physics_knowledge.json"
VECTOR_PATH = DATA_DIR / "vectorizer.pkl"
MATRIX_PATH = DATA_DIR / "knowledge_matrix.npz"
INDEX_PATH = DATA_DIR / "knowledge_index.json"


def load_knowledge():
    """Load the physics knowledge base from JSON."""
    with KB_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_index():
    """Load the index (same content as knowledge, but kept separate for clarity)."""
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)