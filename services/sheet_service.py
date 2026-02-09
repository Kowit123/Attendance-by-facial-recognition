import gspread
import yaml
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# ---------- Load Config ----------
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

class GoogleSheetService:
    LATE_AFTER_MINUTES = cfg["time"]["late_after"]
    def __init__(self, cred_path, sheet_key):
        self.start_time = datetime.now()
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            cred_path,
            scopes=scopes
        )

        client = gspread.authorize(creds)
        self.ws = client.open_by_key(sheet_key).sheet1

    #------------------------- หาแถวจากรหัศ นศ. -------------------------
    def find_student_row(self, student_id, student_id_col=2):
        col_values = self.ws.col_values(student_id_col)

        for idx, value in enumerate(col_values):
            if value == student_id:
                return idx + 1  # sheet in  dex เริ่มที่ 1

        return None
    
    #---------------------------- หาคอลัมวันที่ ----------------------------
    def find_today_col(self, header_row=5):
        today = datetime.now().strftime("%d/%m/%Y")
        headers = self.ws.row_values(header_row)

        for idx, value in enumerate(headers):
            if value == today:
                return idx + 1

        return None
    #------------------------------- mark -------------------------------
    def get_attendance_status(self):
        now = datetime.now()
        late_time = self.start_time + timedelta(minutes=self.LATE_AFTER_MINUTES)

        if now <= late_time:
            return "/"
        else:
            return "สาย"


    def mark_attendance(self, student_id):
        row = self.find_student_row(student_id)
        col = self.find_today_col()

        if row is None:
            raise ValueError("Student ID not found")

        if col is None:
            raise ValueError("Today column not found")

        status = self.get_attendance_status()

        self.ws.update_cell(row, col, status)

