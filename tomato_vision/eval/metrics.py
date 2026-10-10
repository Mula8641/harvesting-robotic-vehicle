from tomato_vision.eval.coco_loader import Box
from tomato_vision.eval.matching import iou


def precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def hit_at_one(top_prediction: Box | None, ground_truth: list[Box], iou_threshold: float) -> bool | None:
    if not ground_truth:
        return None
    return top_prediction is not None and any(iou(top_prediction, box) >= iou_threshold for box in ground_truth)
