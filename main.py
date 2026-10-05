"""
QR Code Toolkit

Generate a QR code from any text or link, and read one back either from an
image file or live from your webcam. Uses OpenCV's built-in QR detector,
so there's no extra system library to install for scanning.
"""

import os

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

import qr_logic as logic

ctk.set_appearance_mode("dark")

BG = "#0b0e10"
PANEL = "#171b1e"
ACCENT = "#4fd1c5"


class QRToolkitApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Toolkit")
        self.geometry("760x640")
        self.configure(fg_color=BG)

        self.tabs = ctk.CTkTabview(self, fg_color=BG, segmented_button_fg_color=PANEL,
                                    segmented_button_selected_color="#2a2a30")
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabs.add("Generate")
        self.tabs.add("Scan")

        self._build_generate_tab(self.tabs.tab("Generate"))
        self._build_scan_tab(self.tabs.tab("Scan"))

        self.cap = None

    # -------------------------------------------------------------- generate

    def _build_generate_tab(self, tab):
        tab.configure(fg_color=BG)

        row = ctk.CTkFrame(tab, fg_color=PANEL, corner_radius=12)
        row.pack(fill="x", pady=(0, 16))
        self.text_var = ctk.StringVar()
        ctk.CTkEntry(row, textvariable=self.text_var, width=420,
                     placeholder_text="Text or URL to encode").pack(side="left", padx=16, pady=14)
        ctk.CTkButton(row, text="Generate", fg_color="#2a2a30",
                      command=self._generate).pack(side="left", padx=(0, 16))

        self.qr_label = ctk.CTkLabel(tab, text="", fg_color=PANEL, corner_radius=12)
        self.qr_label.pack(pady=10)

        self.save_btn = ctk.CTkButton(tab, text="Save as PNG", fg_color="#2a2a30",
                                       command=self._save, state="disabled")
        self.save_btn.pack(pady=6)

        self._current_image = None

    def _generate(self):
        text = self.text_var.get().strip()
        if not text:
            return
        image = logic.make_qr(text)
        self._current_image = image
        preview = image.copy()
        preview.thumbnail((360, 360))
        photo = ImageTk.PhotoImage(preview)
        self.qr_label.configure(image=photo)
        self.qr_label.image = photo
        self.save_btn.configure(state="normal")

    def _save(self):
        if self._current_image is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG image", "*.png")])
        if path:
            self._current_image.save(path)

    # ------------------------------------------------------------------ scan

    def _build_scan_tab(self, tab):
        tab.configure(fg_color=BG)

        controls = ctk.CTkFrame(tab, fg_color=PANEL, corner_radius=12)
        controls.pack(fill="x", pady=(0, 16))
        ctk.CTkButton(controls, text="Scan from image", fg_color="#2a2a30",
                      command=self._scan_image).pack(side="left", padx=16, pady=14)
        self.webcam_btn = ctk.CTkButton(controls, text="Start webcam scan", fg_color="#2a2a30",
                                         command=self._toggle_webcam)
        self.webcam_btn.pack(side="left", padx=(0, 16))

        self.scan_video_label = ctk.CTkLabel(tab, text="", fg_color=PANEL, corner_radius=12)
        self.scan_video_label.pack(pady=10)

        ctk.CTkLabel(tab, text="Decoded result", text_color=ACCENT).pack(anchor="w")
        self.result_var = ctk.StringVar(value="Nothing scanned yet")
        ctk.CTkLabel(tab, textvariable=self.result_var, wraplength=680, justify="left").pack(anchor="w", pady=(4, 10))

        self.scanning = False

    def _scan_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return
        text = logic.decode_image_file(path)
        self.result_var.set(text or "No QR code found in that image")

    def _toggle_webcam(self):
        import cv2
        if self.scanning:
            self.scanning = False
            self.webcam_btn.configure(text="Start webcam scan")
            if self.cap:
                self.cap.release()
                self.cap = None
            return

        self.scanning = True
        self.webcam_btn.configure(text="Stop webcam scan")
        self.cap = cv2.VideoCapture(0)
        self._scan_loop()

    def _scan_loop(self):
        import cv2
        if not self.scanning or self.cap is None:
            return
        ok, frame = self.cap.read()
        if ok:
            text = logic.decode_frame(frame)
            if text:
                self.result_var.set(text)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((640, 400))
            photo = ImageTk.PhotoImage(img)
            self.scan_video_label.configure(image=photo)
            self.scan_video_label.image = photo

        self.after(30, self._scan_loop)

    def destroy(self):
        if self.cap:
            self.cap.release()
        super().destroy()


if __name__ == "__main__":
    app = QRToolkitApp()
    app.mainloop()