from dataclasses import dataclass

from tomato_vision.eval.coco_loader import Box


@dataclass(frozen=True)
class MatchResult:
    true_positives: int
    false_positives: int
    false_negatives: int


def iou(box_a: Box, box_b: Box) -> float:
    inter_width = min(box_a.x2, box_b.x2) - max(box_a.x1, box_b.x1)
    inter_height = min(box_a.y2, box_b.y2) - max(box_a.y1, box_b.y1)
    intersection = max(inter_width, 0) * max(inter_height, 0)
    area_a = (box_a.x2 - box_a.x1) * (box_a.y2 - box_a.y1)
    area_b = (box_b.x2 - box_b.x1) * (box_b.y2 - box_b.y1)
    union = area_a + area_b - intersection
    return intersection / union if union > 0 else 0.0


def match_boxes(predictions: list[Box], ground_truth: list[Box], iou_threshold: float) -> MatchResult:
    unmatched = list(range(len(ground_truth)))
    true_positives = 0
    for prediction in predictions:
        best_index, best_iou = None, iou_threshold
        for index in unmatched:
            overlap = iou(prediction, ground_truth[index])
            if overlap >= best_iou:
                best_index, best_iou = index, overlap
        if best_index is not None:
            unmatched.remove(best_index)
            true_positives += 1
    return MatchResult(true_positives, len(predictions) - true_positives, len(unmatched))
