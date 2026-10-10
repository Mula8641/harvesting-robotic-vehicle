import pytest

from tomato_vision.config.presets import ORIGINAL_CONTROL as CONTROL
from tomato_vision.control.align import Command
from tomato_vision.sim.alignment_sim import simulate_alignment


@pytest.mark.parametrize("start", [(250, 127), (5, 127), (127, 5), (127, 250), (127, 127), (10, 240)])
def test_simulation_ends_in_pick_inside_deadband(start):
    steps = simulate_alignment(start, CONTROL, 5.0, 200)
    final = steps[-1]
    assert final.command is Command.PICK
    assert abs(final.target_center_px[0] - 127.5) <= CONTROL.deadband_px + 1
    assert abs(final.target_center_px[1] - 127.5) <= CONTROL.deadband_px + 1


def test_centered_start_picks_at_tick_zero():
    assert len(simulate_alignment((127, 127), CONTROL, 5.0, 10)) == 1


def test_max_ticks_limits_run():
    steps = simulate_alignment((250, 127), CONTROL, 1.0, 5)
    assert len(steps) == 5 and steps[-1].command is not Command.PICK
