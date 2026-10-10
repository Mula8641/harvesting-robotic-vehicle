import json

import pytest

from tomato_vision.eval.coco_loader import Box, load_ground_truth
from tomato_vision.eval.matching import iou, match_boxes
from tomato_vision.eval.metrics import hit_at_one, precision_recall_f1

A = Box(0, 0, 10, 10)


def test_iou_identical_and_disjoint():
    assert iou(A, A) == 1.0
    assert iou(A, Box(20, 20, 30, 30)) == 0.0


def test_iou_known_overlap():
    assert iou(A, Box(5, 0, 15, 10)) == pytest.approx(50 / 150)


def test_match_cannot_reuse_ground_truth():
    result = match_boxes([A, A], [A], 0.5)
    assert (result.true_positives, result.false_positives, result.false_negatives) == (1, 1, 0)


def test_match_counts_misses():
    result = match_boxes([Box(50, 50, 60, 60)], [A], 0.5)
    assert (result.true_positives, result.false_positives, result.false_negatives) == (0, 1, 1)


def test_precision_recall_f1_worked_example():
    precision, recall, f1 = precision_recall_f1(120, 150, 10)
    assert precision == pytest.approx(120 / 270)
    assert recall == pytest.approx(120 / 130)
    assert f1 == pytest.approx(2 * precision * recall / (precision + recall))


def test_zero_denominators():
    assert precision_recall_f1(0, 0, 0) == (0.0, 0.0, 0.0)


def test_hit_at_one():
    assert hit_at_one(A, [], 0.5) is None
    assert hit_at_one(A, [A], 0.5) is True
    assert hit_at_one(None, [A], 0.5) is False
    assert hit_at_one(Box(50, 50, 60, 60), [A], 0.5) is False


@pytest.fixture
def coco_file(tmp_path):
    data = {
        "images": [{"id": 1, "file_name": "a.jpg"}, {"id": 2, "file_name": "b.jpg"}, {"id": 3, "file_name": "c.jpg"}],
        "categories": [{"id": 1, "name": "b_fully_ripened"}, {"id": 2, "name": "b_green"}],
        "annotations": [
            {"image_id": 1, "category_id": 1, "bbox": [10, 20, 30, 40]},
            {"image_id": 2, "category_id": 1, "segmentation": [[5, 5, 25, 8, 15, 30]]},
            {"image_id": 3, "category_id": 2, "bbox": [0, 0, 5, 5]},
        ],
    }
    path = tmp_path / "ann.json"
    path.write_text(json.dumps(data))
    return path


def test_loader_converts_bbox_and_polygon(coco_file):
    boxes = load_ground_truth(coco_file, frozenset({"b_fully_ripened"}))
    assert boxes["a.jpg"] == [Box(10, 20, 40, 60)]
    assert boxes["b.jpg"] == [Box(5, 5, 25, 30)]
    assert boxes["c.jpg"] == []


def test_loader_missing_class_lists_categories(coco_file):
    with pytest.raises(KeyError, match="b_green"):
        load_ground_truth(coco_file, frozenset({"nope"}))


def test_loader_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_ground_truth(tmp_path / "missing.json", frozenset({"x"}))


def test_predict_boxes_unflips_original_preset():
    import numpy as np
    from tests.helpers import disc_image
    from tomato_vision.config.presets import ORIGINAL
    from tomato_vision.eval.scoring import predict_boxes
    box = predict_boxes(disc_image([(60, 60, 30)]), ORIGINAL, 640)[0]
    assert (box.y1 + box.y2) / 2 == pytest.approx(60, abs=1)
