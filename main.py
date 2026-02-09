import cv2
import yaml
from insightface.app import FaceAnalysis

from core.recognizer import FaceRecognizer
from utils.attendance_guard import AttendanceGuard
from services.sheet_service import GoogleSheetService

# ---------- Load Config ----------
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# ---------- Init Face Engine ----------
provider = cfg["face_engine"]["provider"]
model = cfg["face_engine"]["model"]
# map provider → ctx_id
ctx_id = 0 if provider == "CUDAExecutionProvider" else -1
app = FaceAnalysis(
    name=model,
    providers=[provider]
)
app.prepare(ctx_id=ctx_id)

# ---------- Recognizer ----------
recognizer = FaceRecognizer(
    emb_path="data/embeddings/students.pkl",
    threshold=cfg["recognition"]["threshold"]
)

# ---------- Guard ----------
guard = AttendanceGuard(
    cooldown_seconds=3600
)

# ---------- Sheet ----------
sheet = GoogleSheetService(
    cred_path="api/service_account.json",
    sheet_key=cfg["google_sheet"]["sheet_key"]
)

# ---------- Camera ----------
cap = cv2.VideoCapture(cfg["camera"]["index"])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        emb = face.embedding
        student_id, score = recognizer.recognize(emb)

        x1, y1, x2, y2 = map(int, face.bbox)

        if student_id:
            label = f"{student_id} ({score:.2f})"
            color = (0, 255, 0)

            # ===== Attendance Logic =====
            if guard.can_mark(student_id):
                try:
                    sheet.mark_attendance(student_id)
                    guard.mark(student_id)
                    print(f"{student_id} checked in")

                except Exception as e:
                    print("[ERROR]", e)

        else:
            label = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
