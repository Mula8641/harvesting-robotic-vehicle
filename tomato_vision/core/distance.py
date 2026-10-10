def estimate_distance_cm(width_px: int, focal_length_px: float, real_width_cm: float) -> float:
    if width_px <= 0:
        raise ValueError(f"width_px must be positive, got {width_px}")
    return real_width_cm * focal_length_px / width_px
