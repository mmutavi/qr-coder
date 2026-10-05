"""
Thin wrappers around qrcode (generation) and OpenCV's built-in QR detector
(decoding), so main.py doesn't need to know the details of either library.
"""

import cv2
import numpy as np
import qrcode