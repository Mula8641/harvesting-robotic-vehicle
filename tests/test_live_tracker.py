import numpy as np
import pytest

from tests.helpers import disc_image
from tomato_vision.app.live_tracker import run_loop
from tomato_vision.control.align import Command


class FakeCapture:
    def __init__(self, frames):
        self.frames = list(frames)

    def read(self):
        return (True, self.frames.pop(0)) if self.frames else (False, None)


def test_sends_only_on_change_then_camera_failure_raises():
    empty = np.full((255, 255, 3), 90, dtype=np.uint8)
    centred = disc_image([(127, 127, 20)])
    sent = []
    with pytest.raises(RuntimeError):
        run_loop(FakeCapture([empty, empty, centred, centred]), "advanced", sent.append, show_window=False)
    assert sent == [Command.STOP, Command.PICK]
