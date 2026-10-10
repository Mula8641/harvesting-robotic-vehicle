import numpy as np

from tomato_vision.config.presets import ORIGINAL, ORIGINAL_CONTROL, ADVANCED
from tomato_vision.config.settings import HsvRange
from tomato_vision.core.preprocess import brighten, flip_vertical


def test_original_preset_matches_the_script():
    assert ORIGINAL.hue_ranges == (HsvRange((0, 47, 40), (14, 255, 255)),)
    assert ORIGINAL.brightness_offset == 50
    assert ORIGINAL.flip_vertical is True
    assert ORIGINAL.morph_kernel_px == 0
    assert ORIGINAL.min_area_px == 1
    assert ORIGINAL.keep_largest_only is True


def test_original_control_matches_the_script():
    assert (ORIGINAL_CONTROL.frame_width_px, ORIGINAL_CONTROL.frame_height_px) == (255, 255)
    assert ORIGINAL_CONTROL.deadband_px == 40
    assert ORIGINAL_CONTROL.focal_length_px == 520
    assert ORIGINAL_CONTROL.real_width_cm == 4


def test_advanced_has_two_hue_ranges():
    assert len(ADVANCED.hue_ranges) == 2


def test_brighten_clips_at_255():
    image = np.full((2, 2, 3), 240, dtype=np.uint8)
    result = brighten(image, 50)
    assert result.dtype == np.uint8
    assert (result == 255).all()


def test_brighten_zero_is_identity():
    image = np.arange(12, dtype=np.uint8).reshape(2, 2, 3)
    assert np.array_equal(brighten(image, 0), image)


def test_brighten_negative_clips_at_zero():
    assert (brighten(np.full((1, 1, 3), 10, dtype=np.uint8), -50) == 0).all()


def test_flip_vertical_reverses_rows():
    image = np.arange(12, dtype=np.uint8).reshape(2, 2, 3)
    assert np.array_equal(flip_vertical(image), image[::-1])
