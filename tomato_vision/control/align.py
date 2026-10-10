from enum import Enum, auto

from tomato_vision.config.settings import ControlConfig
from tomato_vision.core.candidates import Detection


class Command(Enum):
    TARGET_RIGHT = auto()
    TARGET_LEFT = auto()
    ADVANCE = auto()
    STOP = auto()
    PICK = auto()


def decide_command(detection: Detection | None, control: ControlConfig) -> Command:
    if detection is None:
        return Command.STOP
    half_width = control.frame_width_px / 2
    half_height = control.frame_height_px / 2
    if detection.center_x > half_width + control.deadband_px:
        command = Command.TARGET_RIGHT
    elif detection.center_x < half_width - control.deadband_px:
        command = Command.TARGET_LEFT
    elif abs(detection.center_y - half_height) > control.deadband_px:
        command = Command.ADVANCE
    else:
        command = Command.PICK
    return command
