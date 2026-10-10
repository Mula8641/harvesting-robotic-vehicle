from dataclasses import dataclass


@dataclass(frozen=True)
class HsvRange:
    lower: tuple[int, int, int]
    upper: tuple[int, int, int]


@dataclass(frozen=True)
class DetectorConfig:
    hue_ranges: tuple[HsvRange, ...]
    brightness_offset: int
    flip_vertical: bool
    morph_kernel_px: int  # 0 disables morphology
    morph_open_iterations: int
    morph_close_iterations: int
    min_area_px: int
    keep_largest_only: bool


@dataclass(frozen=True)
class ControlConfig:
    frame_width_px: int
    frame_height_px: int
    deadband_px: int
    focal_length_px: float
    real_width_cm: float
