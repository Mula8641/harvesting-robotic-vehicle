import argparse
import sys
from typing import Callable

import cv2

from tomato_vision.app.http_sender import send_state
from tomato_vision.config.presets import ORIGINAL_CONTROL, PRESETS
from tomato_vision.control.align import Command, decide_command
from tomato_vision.core.pipeline import detect_tomatoes
from tomato_vision.io.overlay import draw_detections
from tomato_vision.utils.log import get_logger

log = get_logger(__name__)
SEND_TIMEOUT_S = 1.0

Sender = Callable[[Command], object]


def run_loop(capture, preset_name: str, sender: Sender, show_window: bool = True) -> int:
    # Edge triggered like the original flag `a`: send only when the command changes.
    config = PRESETS[preset_name]
    last_sent = None
    while True:
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError("camera read failed")
        detections = detect_tomatoes(frame, config)
        command = decide_command(detections[0] if detections else None, ORIGINAL_CONTROL)
        if command != last_sent:
            sender(command)
            log.info("command %s", command.name)
            last_sent = command
        if show_window:
            cv2.imshow("Frame", draw_detections(frame, detections, None))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="original")
    parser.add_argument("--base-url", default="http://192.168.4.1/")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    capture = cv2.VideoCapture(args.camera)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, ORIGINAL_CONTROL.frame_width_px)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, ORIGINAL_CONTROL.frame_height_px)
    if args.dry_run:
        sender: Sender = lambda command: print(command.name)
    else:
        sender = lambda command: send_state(args.base_url, command, SEND_TIMEOUT_S)
    try:
        code = run_loop(capture, args.preset, sender)
    except (OSError, RuntimeError) as error:
        log.error("stopping robot: %s", error)
        try:
            sender(Command.STOP)
        except OSError:
            log.error("stop command could not be delivered")
        code = 1
    finally:
        capture.release()
        cv2.destroyAllWindows()
    return code


if __name__ == "__main__":
    sys.exit(main())
