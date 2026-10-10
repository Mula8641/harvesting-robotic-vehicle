import cv2
import numpy as np

from tomato_vision.core.candidates import Detection

_GREEN_BGR = (0, 255, 0)


def draw_detections(image_bgr: np.ndarray, detections: list[Detection], label_text: str | None) -> np.ndarray:
    canvas = image_bgr.copy()
    for detection in detections:
        x1, y1, x2, y2 = detection.box
        cv2.rectangle(canvas, (x1, y1), (x2, y2), _GREEN_BGR, 2)
    if label_text is not None:
        cv2.putText(canvas, label_text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, _GREEN_BGR, 2)
    return canvas
