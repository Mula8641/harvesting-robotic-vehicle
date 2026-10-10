import argparse
import json
import sys
from pathlib import Path

import cv2

from tomato_vision.config.presets import PRESETS
from tomato_vision.core.pipeline import detect_tomatoes
from tomato_vision.io.images import list_images, read_bgr
from tomato_vision.io.overlay import draw_detections
from tomato_vision.utils.log import get_logger

log = get_logger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="v2")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    records, failed = {}, 0
    for path in list_images(args.input_dir):
        try:
            image = read_bgr(path)
        except ValueError as error:
            log.error("%s", error)
            failed += 1
            continue
        detections = detect_tomatoes(image, PRESETS[args.preset])
        records[path.name] = [{"box": d.box, "area": d.area} for d in detections]
        overlay = draw_detections(image, detections, f"{args.preset}: {len(detections)} detections")
        cv2.imwrite(str(args.out / f"{path.stem}_{args.preset}.png"), overlay)
    (args.out / "detections.json").write_text(json.dumps(records, indent=2))
    log.info("processed %d images, %d failed", len(records), failed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
