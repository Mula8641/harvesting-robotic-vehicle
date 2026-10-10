from pathlib import Path

import cv2
import numpy as np

_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def list_images(directory: Path) -> list[Path]:
    return sorted(path for path in directory.iterdir() if path.suffix.lower() in _EXTENSIONS)


def read_bgr(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"cannot decode image: {path}")
    return image
