from tomato_vision.config.settings import ControlConfig, DetectorConfig, HsvRange

ORIGINAL = DetectorConfig(
    hue_ranges=(HsvRange((0, 47, 40), (14, 255, 255)),),
    brightness_offset=50,
    flip_vertical=True,
    morph_kernel_px=0,
    morph_open_iterations=0,
    morph_close_iterations=0,
    min_area_px=1,
    keep_largest_only=True,
)

# Chosen by grid search on the Laboro train split (maximum F1): see results/tuning_train.json.
V2 = DetectorConfig(
    hue_ranges=(
        HsvRange((0, 120, 60), (10, 255, 255)),
        HsvRange((169, 120, 60), (179, 255, 255)),
    ),
    brightness_offset=0,
    flip_vertical=False,
    morph_kernel_px=5,
    morph_open_iterations=1,
    morph_close_iterations=2,
    min_area_px=400,
    keep_largest_only=False,
)

ORIGINAL_CONTROL = ControlConfig(
    frame_width_px=255,
    frame_height_px=255,
    deadband_px=40,
    focal_length_px=520.0,
    real_width_cm=4.0,
)

PRESETS = {"original": ORIGINAL, "v2": V2}
