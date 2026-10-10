import cv2
import numpy as np

RED_BGR = (0, 0, 255)
GREEN_BGR = (0, 255, 0)
BLUE_BGR = (255, 0, 0)


def disc_image(discs: list[tuple[int, int, int]], color_bgr=RED_BGR, size: int = 255, background=(90, 90, 90)) -> np.ndarray:
    image = np.full((size, size, 3), background, dtype=np.uint8)
    for center_x, center_y, radius in discs:
        cv2.circle(image, (center_x, center_y), radius, color_bgr, -1)
    return image
