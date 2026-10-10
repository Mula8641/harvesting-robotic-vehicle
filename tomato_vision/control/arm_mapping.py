from dataclasses import dataclass


@dataclass(frozen=True)
class ServoAngles:
    base: int
    shoulder: int
    elbow: int
    wrist: int


def arduino_map(value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    numerator = (value - in_min) * (out_max - out_min)
    denominator = in_max - in_min
    quotient = abs(numerator) // abs(denominator)  # C division truncates toward zero
    if (numerator < 0) != (denominator < 0):
        quotient = -quotient
    return quotient + out_min


def track_angles(x_px: int, y_px: int) -> tuple[int, int, int]:
    base = arduino_map(x_px, 0, 255, 20, 160)
    shoulder = arduino_map(y_px, 0, 255, 50, 150)
    elbow = arduino_map(y_px, 0, 255, 50, 180)
    return base, shoulder, elbow


def pick_wrist_angle(z_px: int) -> int:
    return arduino_map(z_px, 0, 255, 50, 150)
