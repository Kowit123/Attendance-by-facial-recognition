import pickle
import numpy as np
from numpy.linalg import norm

class FaceRecognizer:
    def __init__(self, emb_path, threshold=0.5):
        with open(emb_path, "rb") as f:
            self.db = pickle.load(f)

        self.threshold = threshold

    def cosine(self, a, b):
        return a @ b / (norm(a) * norm(b))

    def recognize(self, emb):
        best_name = None
        best_score = 0

        for student_id, ref_emb in self.db.items():
            score = self.cosine(emb, ref_emb)
            if score > best_score:
                best_score = score
                best_name = student_id

        if best_score >= self.threshold:
            return best_name, best_score

        return None, best_score
