import cv2
import numpy as np
import pytest

from tests.helpers import disc_image
from tomato_vision.config.presets import ORIGINAL, ADVANCED
from tomato_vision.core.candidates import Detection, find_candidates
from tomato_vision.core.distance import estimate_distance_cm
from tomato_vision.core.pipeline import detect_tomatoes


def two_disc_mask() -> np.ndarray:
    mask = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(mask, (50, 50), 20, 255, -1)
    cv2.circle(mask, (150, 150), 10, 255, -1)
    return mask


def test_two_discs_sorted_by_area():
    detections = find_candidates(two_disc_mask(), 1, False)
    assert len(detections) == 2
    assert detections[0].area > detections[1].area


def test_keep_largest_only():
    assert len(find_candidates(two_disc_mask(), 1, True)) == 1


def test_small_blob_dropped():
    detections = find_candidates(two_disc_mask(), 500, False)
    assert len(detections) == 1 and detections[0].center_x == pytest.approx(50, abs=1)


def test_empty_mask_gives_empty_list():
    assert find_candidates(np.zeros((10, 10), dtype=np.uint8), 1, False) == []


def test_box_and_center_of_known_disc():
    detection = find_candidates(two_disc_mask(), 500, False)[0]
    assert detection.center_x == pytest.approx(50, abs=1)
    assert detection.center_y == pytest.approx(50, abs=1)
    assert detection.width == pytest.approx(41, abs=1)
    assert detection.box == (detection.x, detection.y, detection.x + detection.width, detection.y + detection.height)


def test_distance_original_constants():
    assert estimate_distance_cm(104, 520, 4) == pytest.approx(20.0)


def test_distance_zero_width_raises():
    with pytest.raises(ValueError):
        estimate_distance_cm(0, 520, 4)


def test_pipeline_original_keeps_largest_only():
    image = disc_image([(60, 60, 30), (190, 190, 15)])
    detections = detect_tomatoes(image, ORIGINAL)
    assert len(detections) == 1
    # ORIGINAL flips vertically, so the larger disc at y=60 appears at y=194
    assert detections[0].center_y == pytest.approx(194, abs=1)


def test_pipeline_advanced_returns_both():
    assert len(detect_tomatoes(disc_image([(60, 60, 30), (190, 190, 15)]), ADVANCED)) == 2


def test_detection_is_frozen():
    with pytest.raises(AttributeError):
        Detection(0, 0, 1, 1, 1.0).x = 3
