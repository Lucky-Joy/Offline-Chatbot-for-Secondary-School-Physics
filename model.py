import json
import pickle
from typing import List, Tuple, Optional

import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity

from data_loader import VECTOR_PATH, MATRIX_PATH, INDEX_PATH


class PhysicsModel:
    def __init__(self):
        with VECTOR_PATH.open("rb") as f:
            self.vectorizer = pickle.load(f)
        self.matrix = load_npz(MATRIX_PATH)
        with INDEX_PATH.open("r", encoding="utf-8") as f:
            self.kb = json.load(f)

    def query(
        self,
        question: str,
        class_level: Optional[int] = None,
        topic: Optional[str] = None,
        top_k: int = 3,
        min_sim: float = 0.3,
    ) -> Tuple[Optional[Tuple[float, dict]], List[Tuple[float, dict]]]:
        q = (question or "").strip()
        if not q:
            return None, []

        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.matrix)[0]
        idxs = np.argsort(sims)[::-1]

        results: List[Tuple[float, dict]] = []

        for i in idxs:
            sim = float(sims[i])
            if sim < min_sim:
                break
            entry = self.kb[int(i)]

            if class_level is not None and entry.get("class_level") != class_level:
                continue
            if topic is not None and entry.get("topic") != topic:
                continue

            results.append((sim, entry))
            if len(results) >= top_k:
                break

        if not results:
            return None, []

        best = results[0]
        related = results[1:]
        
        return best, related