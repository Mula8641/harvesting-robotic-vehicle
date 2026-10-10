import numpy as np

from tomato_vision.config.settings import DetectorConfig
from tomato_vision.core.candidates import Detection, find_candidates
from tomato_vision.core.preprocess import brighten, flip_vertical
from tomato_vision.core.red_mask import build_red_mask, clean_mask


def detect_tomatoes(image_bgr: np.ndarray, config: DetectorConfig) -> list[Detection]:
    image = flip_vertical(image_bgr) if config.flip_vertical else image_bgr
    image = brighten(image, config.brightness_offset)
    mask = build_red_mask(image, config.hue_ranges)
    mask = clean_mask(mask, config.morph_kernel_px, config.morph_open_iterations, config.morph_close_iterations)
    return find_candidates(mask, config.min_area_px, config.keep_largest_only)
