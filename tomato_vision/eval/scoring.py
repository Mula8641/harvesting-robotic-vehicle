import logging
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from tomato_vision.config.settings import DetectorConfig
from tomato_vision.core.pipeline import detect_tomatoes
from tomato_vision.eval.coco_loader import Box
from tomato_vision.eval.matching import match_boxes
from tomato_vision.eval.metrics import hit_at_one
from tomato_vision.io.images import read_bgr

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class SplitScore:
    tp: int
    fp: int
    fn: int
    hits: int
    hit_images: int
    images: int
    images_skipped: int


def _downscale(image_bgr: np.ndarray, max_side: int) -> tuple[np.ndarray, float]:
    scale = min(1.0, max_side / max(image_bgr.shape[:2]))
    if scale < 1.0:
        image_bgr = cv2.resize(image_bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    return image_bgr, scale


def predict_boxes(image_bgr: np.ndarray, config: DetectorConfig, max_side: int) -> list[Box]:
    # The dataset images are 12 MP: detect on a downscaled copy, report boxes in original pixels.
    small, scale = _downscale(image_bgr, max_side)
    height = small.shape[0]
    boxes = []
    for detection in detect_tomatoes(small, config):
        x1, y1, x2, y2 = detection.box
        if config.flip_vertical:  # boxes come back in the flipped frame; dataset photos are upright
            y1, y2 = height - y2, height - y1
        boxes.append(Box(x1 / scale, y1 / scale, x2 / scale, y2 / scale))
    return boxes


def score_split(
    images_dir: Path, ground_truth: dict[str, list[Box]], config: DetectorConfig, max_side: int, iou_threshold: float
) -> SplitScore:
    tp = fp = fn = hits = hit_images = skipped = 0
    for file_name, truth in ground_truth.items():
        try:
            image = read_bgr(images_dir / file_name)
        except ValueError as error:
            log.warning("skipping image: %s", error)
            skipped += 1
            continue
        predictions = predict_boxes(image, config, max_side)
        match = match_boxes(predictions, truth, iou_threshold)
        tp, fp, fn = tp + match.true_positives, fp + match.false_positives, fn + match.false_negatives
        hit = hit_at_one(predictions[0] if predictions else None, truth, iou_threshold)
        if hit is not None:
            hit_images += 1
            hits += hit
    return SplitScore(tp, fp, fn, hits, hit_images, len(ground_truth) - skipped, skipped)
