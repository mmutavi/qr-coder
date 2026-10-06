"""
Thin wrappers around qrcode (generation) and OpenCV's built-in QR detector
(decoding), so main.py doesn't need to know the details of either library.
"""

import cv2
import numpy as np
import qrcode


def make_qr(text):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def decode_frame(frame):
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(frame)
    return data if data else None