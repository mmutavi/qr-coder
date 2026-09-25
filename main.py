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