import numpy as np

from tests.helpers import BLUE_BGR, GREEN_BGR, disc_image
from tomato_vision.config.presets import ORIGINAL, V2
from tomato_vision.core.red_mask import build_red_mask, clean_mask


def test_red_disc_detected_by_both_presets():
    image = disc_image([(128, 128, 30)])
    for preset in (ORIGINAL, V2):
        assert build_red_mask(image, preset.hue_ranges)[128, 128] == 255


def test_hue_175_only_in_v2():
    pixel_bgr = np.full((1, 1, 3), 0, dtype=np.uint8)
    import cv2
    pixel_bgr = cv2.cvtColor(np.array([[[175, 200, 200]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)
    assert build_red_mask(pixel_bgr, V2.hue_ranges)[0, 0] == 255
    assert build_red_mask(pixel_bgr, ORIGINAL.hue_ranges)[0, 0] == 0


def test_green_and_blue_give_empty_mask():
    for color in (GREEN_BGR, BLUE_BGR):
        mask = build_red_mask(disc_image([(128, 128, 30)], color_bgr=color, background=(0, 0, 0)), V2.hue_ranges)
        assert mask.sum() == 0


def test_clean_mask_kernel_zero_is_unchanged():
    mask = np.zeros((20, 20), dtype=np.uint8)
    mask[5, 5] = 255
    assert np.array_equal(clean_mask(mask, 0, 1, 2), mask)


def test_clean_mask_removes_speck_keeps_disc():
    import cv2
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[10:12, 10:12] = 255
    cv2.circle(mask, (60, 60), 20, 255, -1)
    cleaned = clean_mask(mask, 5, 1, 2)
    assert cleaned[10:12, 10:12].sum() == 0
    assert cleaned[60, 60] == 255
