# Face Attendance

ระบบจดจำใบหน้า (Face Attendance) สำหรับบันทึกการเข้าเรียน/เข้างานด้วยการจับคู่ embeddings ใบหน้า

**โครงสร้างโปรเจค (พื้นฐาน)**
- [main.py](main.py) — จุดเริ่มต้นของแอป
- [nui.py](nui.py) — อินเทอร์เฟซกราฟิก (ถ้ามี)
- [scripts/build_embeddings.py](scripts/build_embeddings.py) — สร้าง/ปรับปรุง embeddings จากโฟลเดอร์ `data/students`
- `data/embeddings/` — เก็บไฟล์ embeddings ที่สร้างแล้ว
- `data/students/` — รูปภาพนักเรียน/พนักงาน แยกตามรหัส
- [api/service_account.json](api/service_account.json) — กุญแจบริการสำหรับ Google Sheets (ถ้าใช้งาน)
- [config.yaml](config.yaml) — การตั้งค่าของโปรเจค (เช่น Google Sheets ID, thresholds)

## ข้อกำหนดเบื้องต้น
- Python 3.8+ (แนะนำ 3.10+)
- virtual environment (`venv`)
- ไลบรารีที่จำเป็น — ระบุไว้ใน `requirements.txt` (ถ้ามี)

## ตั้งค่า (Windows / PowerShell)
1. สร้างและเปิด virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
2. ติดตั้ง dependencies (ถ้ามี `requirements.txt`)
```powershell
pip install -r requirements.txt
```

## การตั้งค่าเพิ่มเติม
- วางไฟล์กุญแจ Google Service Account ที่ได้จาก Google Cloud ใน [api/service_account.json](api/service_account.json) ถ้าแอปเชื่อมกับ Google Sheets
- แก้ไขการตั้งค่าใน [config.yaml](config.yaml) ให้ตรงกับ environment ของคุณ (เช่น spreadsheet ID, threshold, พารามิเตอร์อื่น ๆ)

## การสร้าง embeddings
เมื่อเตรียมรูปภาพนักเรียนเรียบร้อย (ตัวอย่างโฟลเดอร์: `data/students/<id>/`)
```powershell
python scripts\build_embeddings.py
```
ผลลัพธ์จะถูกเขียนไปที่ `data/embeddings/`

## การรันแอป
- แบบเร็ว (Windows): ดับเบิลคลิก `start.bat` หรือเรียกจาก PowerShell
```powershell
.\start.bat
```
- หรือรันโดยตรง
```powershell
python main.py
```

## โฟลเดอร์ข้อมูลสำคัญ
- `data/students/` — รูปภาพต้นทางของแต่ละคน (ใช้สร้าง embeddings)
- `data/embeddings/` — embeddings ที่สร้างขึ้น

## หมายเหตุและแนวทางแก้ปัญหาเบื้องต้น
- ถ้าหาไลบรารีไม่พบ ให้ตรวจสอบว่าเปิด venv แล้วและติดตั้ง dependencies ถูกต้อง
- ปัญหาเกี่ยวกับ Google Sheets: ตรวจสอบ [api/service_account.json](api/service_account.json) และสิทธิ์การเข้าถึงของ service account
## ขั้นตอนการติดตั้งและใช้งาน (แบบละเอียด)

ต่อไปนี้เป็นขั้นตอนที่แนะนำให้ทำตามเรียงลำดับเพื่อให้โปรเจคพร้อมใช้งานบนเครื่อง Windows

1) เตรียม Python & virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2) ติดตั้ง dependencies (ไฟล์ `requirements.txt` ถูกปักเวอร์ชันไว้เรียบร้อยแล้ว)

```powershell
pip install -r requirements.txt
```

หมายเหตุสั้น ๆ เกี่ยวกับ `requirements.txt`:

- ไฟล์ `requirements.txt` ในรีโปนี้ถูกปักเวอร์ชันตาม environment ที่ทดสอบไว้ (เวอร์ชันเต็มอยู่ในไฟล์) — ติดตั้งตรง ๆ จะช่วยให้ได้ environment ที่คาดการณ์ได้
- แพ็กเกจสำคัญที่โปรเจคใช้งาน:
	- `insightface==0.7.3` — ตัว engine สำหรับดึง embedding ใบหน้า
	- `onnxruntime-gpu==1.16.3` — runtime สำหรับรันโมเดล (ไฟล์นี้ใช้เวอร์ชัน GPU)
	- `numpy==1.26.4`
	- `opencv-python==4.12.0.88` (และ `opencv-python-headless` ด้วยใน venv)
	- `PyYAML==6.0.3` — อ่าน `config.yaml`
	- `gspread==6.2.1`, `google-auth==2.47.0` — เชื่อม Google Sheets

- ถ้ารันบนเครื่องที่ไม่มี GPU: ให้แก้ `requirements.txt` โดยแทนที่ `onnxruntime-gpu==1.16.3` ด้วย `onnxruntime==1.16.3` จากนั้นติดตั้งด้วย `pip install -r requirements.txt` อีกครั้ง
- หากต้องการเฉพาะชุดแพ็กเกจเล็ก ๆ (minimal), ผมสามารถล้าง `requirements.txt` ให้เหลือเฉพาะแพ็กเกจที่โค้ดเรียกใช้จริงและส่งให้คุณได้

3) ตั้งค่าไฟล์ `config.yaml` (ตัวอย่างขั้นต่ำ)

ตัวอย่าง `config.yaml`:

```yaml
face_engine:
	provider: "CPUExecutionProvider"   # หรือ "CUDAExecutionProvider" ถ้ามี GPU/กรณีใช้ onnxruntime-gpu
	model: "buffalo_l"                # ชื่อโมเดล insightface ที่ต้องการใช้

camera:
	index: 0

recognition:
	threshold: 0.5

google_sheet:
	sheet_key: "<YOUR_SPREADSHEET_KEY>"

time:
	late_after: 15  # นาที
```

วางไฟล์ `config.yaml` ที่ root ของโปรเจคและแก้ค่าให้ตรงกับสภาพแวดล้อมของคุณ

4) ตั้งค่า Google Service Account (ถาจะใช้ Google Sheets)

- ไปที่ Google Cloud Console → สร้าง Service Account → สร้าง key (JSON)
- ดาวน์โหลดไฟล์ JSON แล้ววางไว้ที่ `api/service_account.json`
- ให้แชร์ Google Sheet ที่ต้องการให้ service account อนุญาต (เพิ่มอีเมลของ service account เป็น editor)

5) เตรียมภาพนักเรียน

- โฟลเดอร์ต้นทาง: `data/students/<student_id>/` ใส่รูปภาพแต่ละบุคคล
- แนะนำอย่างน้อย 5 รูปต่อคน (มุม/แสงต่างกัน) เพื่อผลลัพธ์ดีกว่า
- รูปที่มีหลายหน้าคนจะถูกข้าม (สคริปต์ต้องการรูปที่มีใบหน้าเดียว)

6) สร้าง embeddings

```powershell
python scripts\build_embeddings.py
```

ผลลัพธ์: `data/embeddings/students.pkl`

7) รันโปรแกรมหลัก (แสดงกล้องและบันทึกการเข้าเรียนนักเรียนไปยัง Google Sheets)

```powershell
python main.py
```

หรือใช้ `start.bat` เพื่อรันแบบรวดเร็ว

8) การตรวจสอบและแก้ปัญหาเบื้องต้น

- ถ้ากล้องไม่ขึ้น: ตรวจสอบ `camera.index` ใน `config.yaml` และสิทธิ์กล้องของระบบ
- ถ้าโมเดล insightface โหลดไม่สำเร็จ: ตรวจสอบว่าติดตั้ง `insightface` และ `onnxruntime(-gpu)` ให้ถูกต้อง
- ถ้าการเขียน Google Sheet ล้มเหลว: ตรวจสอบไฟล์ `api/service_account.json` และการแชร์ spreadsheet
- ดูข้อความในคอนโซลสำหรับ error tracebacks — มักให้คำใบ้สาเหตุ

## หมายเหตุและแนวทางแก้ปัญหาเบื้องต้น
- ถ้าหาไลบรารีไม่พบ ให้ตรวจสอบว่าเปิด venv แล้วและติดตั้ง dependencies ถูกต้อง
- ปัญหาเกี่ยวกับ Google Sheets: ตรวจสอบ [api/service_account.json](api/service_account.json) และสิทธิ์การเข้าถึงของ service account

## ต้องการความช่วยเหลือเพิ่มเติม
ผมสามารถ:
- สร้างตัวอย่าง `config.yaml` จริงให้คุณวางได้ทันที
- ล้าง `requirements.txt` ให้เหลือเฉพาะแพ็กเกจที่โค้ดใช้งานจริง
- ช่วยตั้งค่า Google Service Account ทีละขั้นตอน

บอกผมว่าต้องการตัวอย่างไหนต่อไปครับ
