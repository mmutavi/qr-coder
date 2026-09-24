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