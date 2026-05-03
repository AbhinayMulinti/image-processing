"""
utils.py — Helper functions for image format conversions.
Handles PIL ↔ NumPy ↔ bytes so app.py stays clean.
"""

import io
import numpy as np
from PIL import Image
import cv2


def pil_to_bgr(pil_image: Image.Image) -> np.ndarray:
    """Convert a PIL Image to a NumPy BGR array (OpenCV format)."""
    rgb_array = np.array(pil_image.convert("RGB"))
    bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
    return bgr_array


def bgr_to_rgb(bgr_array: np.ndarray) -> np.ndarray:
    """Convert a NumPy BGR array to RGB for display in Streamlit."""
    return cv2.cvtColor(bgr_array, cv2.COLOR_BGR2RGB)


def bgr_to_bytes(bgr_array: np.ndarray, fmt: str = ".png") -> bytes:
    """Convert a NumPy BGR array to PNG/JPEG bytes for download."""
    success, encoded = cv2.imencode(fmt, bgr_array)
    if not success:
        raise ValueError(f"Failed to encode image to {fmt}")
    return encoded.tobytes()


def load_uploaded_image(uploaded_file) -> np.ndarray:
    """
    Read a Streamlit UploadedFile and return a NumPy BGR array.
    """
    pil_image = Image.open(uploaded_file)
    return pil_to_bgr(pil_image)
