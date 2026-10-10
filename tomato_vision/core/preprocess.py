import cv2
import numpy as np


def brighten(image_bgr: np.ndarray, offset: int) -> np.ndarray:
    return np.clip(image_bgr.astype(np.int16) + offset, 0, 255).astype(np.uint8)


def flip_vertical(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.flip(image_bgr, 0)
