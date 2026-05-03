"""
filters.py — All OpenCV filter functions.
Each function accepts a NumPy BGR image array and returns a processed NumPy BGR array.
"""

import cv2
import numpy as np


def apply_blur(image: np.ndarray, ksize: int) -> np.ndarray:
    """Apply Gaussian blur. ksize must be odd and >= 1."""
    if ksize < 2:
        return image
    # Ensure ksize is odd
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def apply_sharpness(image: np.ndarray, alpha: float) -> np.ndarray:
    """
    Sharpen using unsharp mask technique.
    alpha controls sharpening intensity (0.0 = no sharpening).
    """
    if alpha <= 0.0:
        return image
    # Create a blurred version
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # Unsharp mask: original + alpha * (original - blurred)
    sharpened = cv2.addWeighted(image, 1.0 + alpha, blurred, -alpha, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def apply_brightness(image: np.ndarray, beta: int) -> np.ndarray:
    """Adjust brightness by adding beta to all pixel values. beta: -100 to 100."""
    if beta == 0:
        return image
    return cv2.convertScaleAbs(image, alpha=1.0, beta=beta)


def apply_contrast(image: np.ndarray, alpha: float) -> np.ndarray:
    """Adjust contrast by scaling pixel values around mid-point. alpha: 0.5 to 3.0."""
    if alpha == 1.0:
        return image
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)


def apply_edge_detection(image: np.ndarray, thresh1: int, thresh2: int) -> np.ndarray:
    """
    Apply Canny edge detection.
    Returns a 3-channel BGR image so it can be stacked with other filters.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, thresh1, thresh2)
    # Convert single-channel edges back to 3-channel BGR
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def apply_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert to grayscale and return as 3-channel BGR for display consistency."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_all_filters(
    image: np.ndarray,
    blur_ksize: int = 1,
    sharpness_alpha: float = 0.0,
    brightness_beta: int = 0,
    contrast_alpha: float = 1.0,
    edge_detect: bool = False,
    edge_thresh1: int = 100,
    edge_thresh2: int = 200,
    grayscale: bool = False,
) -> np.ndarray:
    """
    Apply all filters in sequence (stackable).
    Order: Blur → Sharpness → Brightness → Contrast → Grayscale → Edge Detection
    """
    result = image.copy()

    # 1. Blur
    result = apply_blur(result, blur_ksize)

    # 2. Sharpness
    result = apply_sharpness(result, sharpness_alpha)

    # 3. Brightness
    result = apply_brightness(result, brightness_beta)

    # 4. Contrast
    result = apply_contrast(result, contrast_alpha)

    # 5. Grayscale (before edge detection so edges work on grayscale)
    if grayscale:
        result = apply_grayscale(result)

    # 6. Edge Detection
    if edge_detect:
        result = apply_edge_detection(result, edge_thresh1, edge_thresh2)

    return result
