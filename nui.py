import customtkinter as ctk
from tkinter import messagebox
import yaml
import subprocess
import sys

# ตั้งค่าธีมและสีพื้นฐาน
ctk.set_appearance_mode("Dark")  # โหมดมืด
ctk.set_default_color_theme("blue") 

CONFIG_PATH = "config.yaml"
process = None

# ---------- Config Functions ----------
def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"camera": {"index": 0}, "time": {"late_after": 15}, 
                "face_engine": {"provider": "CPUExecutionProvider", "model": "buffalo_l"},
                "recognition": {"threshold": 0.75}, "google_sheet": {"sheet_key": ""}}

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, allow_unicode=True)

cfg = load_config()

# ---------- UI Class ----------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Face Attendance Control Panel")
        self.geometry("500x580")
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Face Attendance System", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(30, 20))

        # Main Container
        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        # Camera Index
        self.create_input_row("📷 Camera Index", "int", "camera_index", cfg["camera"]["index"])
        
        # Late After
        self.create_input_row("⏰ Late After (min)", "int", "late_after", cfg["time"]["late_after"])

        # Execution Provider
        self.create_combo_row("⚙️ Execution Provider", ["CPUExecutionProvider", "CUDAExecutionProvider"], "provider", cfg["face_engine"]["provider"])

        # Model
        self.create_combo_row("🧠 Model Name (Rebuild if changing)", ["buffalo_s", "buffalo_l"], "model", cfg["face_engine"]["model"])

        # Threshold Slider
        self.th_label = ctk.CTkLabel(self.container, text=f"🎯 Recognition Threshold: {cfg['recognition']['threshold']}")
        self.th_label.pack(anchor="w", padx=20)
        self.th_slider = ctk.CTkSlider(self.container, from_=0.2, to=0.9, command=self.update_th_label)
        self.th_slider.set(cfg["recognition"]["threshold"])
        self.th_slider.pack(fill="x", padx=20, pady=(0, 15))

        # Google Sheet Key
        ctk.CTkLabel(self.container, text="🔑 Google Sheet Key").pack(anchor="w", padx=20)
        self.sheet_entry = ctk.CTkEntry(self.container, placeholder_text="Enter key here...", show="•")
        self.sheet_entry.insert(0, cfg["google_sheet"]["sheet_key"])
        self.sheet_entry.pack(fill="x", padx=20, pady=(0, 20))

        # ---------- Buttons ----------
        self.btn_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_grid.pack(pady=20)

        # กำหนดสีปุ่มตามแบบ UI Modern
        self.btn_rebuild = ctk.CTkButton(self.btn_grid, text="🆕 Rebuild", fg_color="#D35400", hover_color="#E67E22", width=100, command=self.new_embeddings)
        self.btn_rebuild.grid(row=0, column=0, padx=5)

        self.btn_save = ctk.CTkButton(self.btn_grid, text="💾 Save", fg_color="#2980B9", width=100, command=self.on_save)
        self.btn_save.grid(row=0, column=1, padx=5)

        self.btn_start = ctk.CTkButton(self.btn_grid, text="▶ Start", fg_color="#27AE60", hover_color="#2ECC71", width=100, command=self.on_start)
        self.btn_start.grid(row=0, column=2, padx=5)

        self.btn_stop = ctk.CTkButton(self.btn_grid, text="⏹ Stop", fg_color="#C0392B", hover_color="#E74C3C", width=100, command=self.on_stop)
        self.btn_stop.grid(row=0, column=3, padx=5)

    def create_input_row(self, label_text, type, attr_name, default_val):
        row = ctk.CTkFrame(self.container, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(row, text=label_text).pack(side="left")
        entry = ctk.CTkEntry(row, width=100)
        entry.insert(0, str(default_val))
        entry.pack(side="right")
        setattr(self, f"entry_{attr_name}", entry)

    def create_combo_row(self, label_text, values, attr_name, default_val):
        row = ctk.CTkFrame(self.container, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(row, text=label_text).pack(side="left")
        combo = ctk.CTkComboBox(row, values=values, width=180)
        combo.set(default_val)
        combo.pack(side="right")
        setattr(self, f"combo_{attr_name}", combo)

    def update_th_label(self, value):
        self.th_label.configure(text=f"🎯 Recognition Threshold: {value:.2f}")

    def on_save(self):
        try:
            cfg["camera"]["index"] = int(self.entry_camera_index.get())
            cfg["face_engine"]["provider"] = self.combo_provider.get()
            cfg["face_engine"]["model"] = self.combo_model.get()
            cfg["recognition"]["threshold"] = round(self.th_slider.get(), 2)
            cfg["google_sheet"]["sheet_key"] = self.sheet_entry.get().strip()
            cfg["time"]["late_after"] = int(self.entry_late_after.get())

            save_config(cfg)
            messagebox.showinfo("Saved", "บันทึกการตั้งค่าเรียบร้อยแล้ว!")
        except ValueError:
            messagebox.showerror("Error", "กรุณากรอกข้อมูลตัวเลขให้ถูกต้อง")

    def on_start(self):
        global process
        if process:
            messagebox.showwarning("Running", "ระบบกำลังทำงานอยู่แล้ว")
            return
        
        self.on_save()
        process = subprocess.Popen([sys.executable, "main.py"])
        messagebox.showinfo("Started", "ระบบเริ่มทำงานแล้ว ")

    def on_stop(self):
        global process
        if not process:
            return
        process.terminate()
        process = None
        messagebox.showinfo("Stopped", "หยุดการทำงานแล้ว")

    def new_embeddings(self):
        if messagebox.askyesno("Confirm", "ต้องการสร้าง Face Embeddings ใหม่ทั้งหมดใช่หรือไม่?"):
            subprocess.Popen([sys.executable, "scripts/build_embeddings.py"])
            messagebox.showinfo("Processing", "กำลังสร้างข้อมูลใน Background...")
            

if __name__ == "__main__":
    app = App()
    app.mainloop()