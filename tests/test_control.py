import pytest

from tomato_vision.config.presets import ORIGINAL_CONTROL as CONTROL
from tomato_vision.control.align import Command, decide_command
from tomato_vision.control.arm_mapping import arduino_map, pick_wrist_angle, track_angles
from tomato_vision.control.protocol import http_query, serial_pick_frame, serial_track_frame
from tomato_vision.core.candidates import Detection


def at(center_x: int, center_y: int) -> Detection:
    return Detection(center_x - 1, center_y - 1, 2, 2, 4.0)


def test_no_detection_stops():
    assert decide_command(None, CONTROL) is Command.STOP


def test_right_left_advance_pick():
    assert decide_command(at(200, 127), CONTROL) is Command.TARGET_RIGHT
    assert decide_command(at(50, 127), CONTROL) is Command.TARGET_LEFT
    assert decide_command(at(127, 20), CONTROL) is Command.ADVANCE
    assert decide_command(at(127, 230), CONTROL) is Command.ADVANCE
    assert decide_command(at(127, 127), CONTROL) is Command.PICK


# Frame centre is 127.5, so the band edge is 87.5 to 167.5 on both axes.
@pytest.mark.parametrize("center_x,expected", [
    (167, Command.PICK), (168, Command.TARGET_RIGHT),
    (88, Command.PICK), (87, Command.TARGET_LEFT),
])
def test_x_deadband_boundary(center_x, expected):
    assert decide_command(at(center_x, 127), CONTROL) is expected


@pytest.mark.parametrize("center_y,expected", [
    (167, Command.PICK), (168, Command.ADVANCE),
    (88, Command.PICK), (87, Command.ADVANCE),
])
def test_y_deadband_boundary(center_y, expected):
    assert decide_command(at(127, center_y), CONTROL) is expected


def test_http_queries():
    assert http_query(Command.TARGET_RIGHT) == "?State=l"
    assert http_query(Command.TARGET_LEFT) == "?State=r"
    assert http_query(Command.ADVANCE) == "?State=f"
    assert http_query(Command.STOP) == "?State=s"
    assert http_query(Command.PICK) == "?State=sa"


def test_serial_frames():
    assert serial_track_frame(5, 200) == "T,005,200"
    assert serial_pick_frame(7) == "P,000,007"


@pytest.mark.parametrize("bad", [-1, 256])
def test_serial_out_of_range(bad):
    with pytest.raises(ValueError):
        serial_track_frame(bad, 0)
    with pytest.raises(ValueError):
        serial_pick_frame(bad)


def test_arduino_map_example():
    assert arduino_map(127, 0, 255, 20, 160) == 89


def test_arduino_map_end_points():
    assert arduino_map(0, 0, 255, 20, 160) == 20
    assert arduino_map(255, 0, 255, 20, 160) == 160
    assert arduino_map(0, 0, 255, 50, 180) == 50
    assert arduino_map(255, 0, 255, 50, 180) == 180


def test_arduino_map_truncates_toward_zero():
    # (1 * -10) / 3 = -3.33; C gives -3 then +0, Python floor division would give -4
    assert arduino_map(1, 0, 3, 0, -10) == -3
    assert (1 * -10) // 3 == -4


def test_track_angles_and_pick_wrist_ranges():
    for value in (0, 100, 255):
        base, shoulder, elbow = track_angles(value, value)
        assert 20 <= base <= 160 and 50 <= shoulder <= 150 and 50 <= elbow <= 180
        assert 50 <= pick_wrist_angle(value) <= 150
