import os
import cv2
import pickle
import numpy as np
import yaml
from insightface.app import FaceAnalysis

DATA_DIR = "data/students"
OUT_PATH = "data/embeddings/students.pkl"

# ---------- Load Config ----------
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# init InsightFace
provider = cfg["face_engine"]["provider"]
model = cfg["face_engine"]["model"]
    # map provider → ctx_id
ctx_id = 0 if provider == "CUDAExecutionProvider" else -1
app = FaceAnalysis(
    name=model,
    providers=[provider]
)
app.prepare(ctx_id=ctx_id)

embedding_db = {}

def normalize(v):
    return v / np.linalg.norm(v)

for student_id in os.listdir(DATA_DIR):
    student_path = os.path.join(DATA_DIR, student_id)

    if not os.path.isdir(student_path):
        continue

    embeddings = []
    print(f"\nProcessing {student_id}")

    for img_name in os.listdir(student_path):
        img_path = os.path.join(student_path, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"  [SKIP] Cannot read {img_name}")
            continue

        faces = app.get(img)

        if len(faces) != 1:
            print(f"  [SKIP] {img_name} (faces={len(faces)})")
            continue

        emb = faces[0].embedding
        emb = normalize(emb)
        embeddings.append(emb)
        print(f"  [OK] {img_name}")

    if len(embeddings) >= 3:
        mean_emb = np.mean(embeddings, axis=0)
        mean_emb = normalize(mean_emb)
        embedding_db[student_id] = mean_emb
        print(f"  ✔ saved ({len(embeddings)} images)")
    else:
        print(f"  ✖ not enough valid images")

# save embeddings
os.makedirs("data/embeddings", exist_ok=True)
with open(OUT_PATH, "wb") as f:
    pickle.dump(embedding_db, f)

print("\nDone. Total students:", len(embedding_db))
print("Saved to:", OUT_PATH)
