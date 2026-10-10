from dataclasses import dataclass

from tomato_vision.config.settings import ControlConfig
from tomato_vision.control.align import Command, decide_command
from tomato_vision.core.candidates import Detection


@dataclass(frozen=True)
class SimStep:
    tick: int
    target_center_px: tuple[float, float]
    command: Command


def _step_toward(value: float, goal: float, step: float) -> float:
    return goal if abs(goal - value) <= step else value + step * (1 if goal > value else -1)


def simulate_alignment(
    start_center_px: tuple[float, float], control: ControlConfig, pixels_per_tick: float, max_ticks: int
) -> list[SimStep]:
    center_x, center_y = start_center_px
    goal_x, goal_y = control.frame_width_px / 2, control.frame_height_px / 2
    steps = []
    for tick in range(max_ticks):
        # Detection holds integer pixels, so the centre is rounded to the nearest pixel.
        target = Detection(round(center_x) - 1, round(center_y) - 1, 2, 2, 4.0)
        command = decide_command(target, control)
        steps.append(SimStep(tick, (center_x, center_y), command))
        if command is Command.PICK:
            break
        if command in (Command.TARGET_RIGHT, Command.TARGET_LEFT):
            center_x = _step_toward(center_x, goal_x, pixels_per_tick)
        elif command is Command.ADVANCE:
            center_y = _step_toward(center_y, goal_y, pixels_per_tick)
    return steps
