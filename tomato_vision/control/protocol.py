from tomato_vision.control.align import Command

# TARGET_RIGHT -> "l" and TARGET_LEFT -> "r" copy the original script on purpose:
# the codes are tied to the vehicle wiring and the vertically flipped camera.
STATE_CODE = {
    Command.TARGET_RIGHT: "l",
    Command.TARGET_LEFT: "r",
    Command.ADVANCE: "f",
    Command.STOP: "s",
    Command.PICK: "sa",
}

_PIXEL_MAX = 255


def http_query(command: Command) -> str:
    return f"?State={STATE_CODE[command]}"


def _check_pixel(value: int) -> int:
    if not 0 <= value <= _PIXEL_MAX:
        raise ValueError(f"pixel value must be 0..{_PIXEL_MAX}, got {value}")
    return value


def serial_track_frame(x_px: int, y_px: int) -> str:
    return f"T,{_check_pixel(x_px):03d},{_check_pixel(y_px):03d}"


def serial_pick_frame(z_px: int) -> str:
    # The firmware reads characters 6 to 8 only, so the middle field is padding.
    return f"P,000,{_check_pixel(z_px):03d}"
