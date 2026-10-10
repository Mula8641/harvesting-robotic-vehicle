import cv2
import numpy as np

from tomato_vision.config.settings import HsvRange


def build_red_mask(image_bgr: np.ndarray, hue_ranges: tuple[HsvRange, ...]) -> np.ndarray:
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for hue_range in hue_ranges:
        mask |= cv2.inRange(hsv, np.array(hue_range.lower), np.array(hue_range.upper))
    return mask


def clean_mask(mask: np.ndarray, kernel_px: int, open_iterations: int, close_iterations: int) -> np.ndarray:
    cleaned = mask
    if kernel_px > 0:
        kernel = np.ones((kernel_px, kernel_px), np.uint8)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel, iterations=open_iterations)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=close_iterations)
    return cleaned
