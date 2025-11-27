import json
import pickle
from pathlib import Path

from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer

from data_loader import (
    DATA_DIR,
    KB_PATH,
    VECTOR_PATH,
    MATRIX_PATH,
    INDEX_PATH,
    load_knowledge,
)


def build():
    print(">>> build() started")
    print(f"DATA_DIR       : {DATA_DIR}")
    print(f"KB_PATH        : {KB_PATH}")
    print(f"VECTOR_PATH    : {VECTOR_PATH}")
    print(f"MATRIX_PATH    : {MATRIX_PATH}")
    print(f"INDEX_PATH     : {INDEX_PATH}")

    if not KB_PATH.exists():
        raise FileNotFoundError(f"Knowledge base file not found: {KB_PATH}")

    kb = load_knowledge()
    print(f"Loaded {len(kb)} entries from knowledge base.")

    texts = []
    for e in kb:
        parts = [
            e.get("question", ""),
            e.get("answer", ""),
            e.get("topic", ""),
            e.get("subtopic", ""),
        ]
        combined = " ".join(parts)
        texts.append(combined)

    if not texts:
        raise ValueError("Knowledge base is empty. Add at least one entry to physics_knowledge.json")

    print("Fitting TfidfVectorizer...")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    print("Vectorizer fitted. Matrix shape:", X.shape)

    DATA_DIR.mkdir(exist_ok=True)

    print("Saving matrix and vectorizer...")
    save_npz(MATRIX_PATH, X)
    with VECTOR_PATH.open("wb") as f:
        pickle.dump(vectorizer, f)

    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(">>> Model built and saved in 'data' folder.")


if __name__ == "__main__":
    print("=== Running build_model.py ===")
    try:
        build()
    except Exception as e:
        print("!!! Error while building model:", repr(e))
        import traceback
        traceback.print_exc()
    print("=== build_model.py finished ===")