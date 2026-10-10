from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class Detection:
    x: int
    y: int
    width: int
    height: int
    area: float

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    @property
    def box(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)


def find_candidates(mask: np.ndarray, min_area_px: int, keep_largest_only: bool) -> list[Detection]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_area_px:
            x, y, width, height = cv2.boundingRect(contour)
            detections.append(Detection(x, y, width, height, area))
    detections.sort(key=lambda detection: detection.area, reverse=True)
    return detections[:1] if keep_largest_only else detections
