import argparse
import dataclasses
import json
import sys
from datetime import date
from pathlib import Path

import cv2
import numpy as np

from tomato_vision.config.presets import PRESETS
from tomato_vision.eval.coco_loader import load_ground_truth
from tomato_vision.eval.metrics import precision_recall_f1
from tomato_vision.eval.scoring import SplitScore, score_split
from tomato_vision.utils.log import get_logger

RIPE_CLASSES = frozenset({"b_fully_ripened", "l_fully_ripened"})
IOU_THRESHOLD = 0.5

log = get_logger(__name__)


def build_report(preset_name: str, split_name: str, score: SplitScore, max_side: int) -> dict:
    precision, recall, f1 = precision_recall_f1(score.tp, score.fp, score.fn)
    return {
        "preset": preset_name, "split": split_name, "images": score.images, "images_skipped": score.images_skipped,
        "tp": score.tp, "fp": score.fp, "fn": score.fn,
        "precision": precision, "recall": recall, "f1": f1,
        "hit_at_1": score.hits / score.hit_images if score.hit_images else 0.0,
        "hit_at_1_images": score.hit_images,
        "iou_threshold": IOU_THRESHOLD, "max_side_px": max_side,
        "config": dataclasses.asdict(PRESETS[preset_name]),
        "date": date.today().isoformat(),
        "versions": {"python": sys.version.split()[0], "opencv": cv2.__version__, "numpy": np.__version__},
    }


def table_row(report: dict) -> str:
    return (f"| {report['preset']} | {report['images']} | {report['tp']} | {report['fp']} | {report['fn']} | "
            f"{report['precision']:.3f} | {report['recall']:.3f} | {report['f1']:.3f} | {report['hit_at_1']:.3f} |")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--preset", choices=sorted(PRESETS), required=True)
    parser.add_argument("--split-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-side", type=int, default=640)
    args = parser.parse_args(argv)
    log.info("evaluating preset=%s split=%s", args.preset, args.split_name)
    ground_truth = load_ground_truth(args.annotations, RIPE_CLASSES)
    log.info("loaded ground truth for %d images", len(ground_truth))
    score = score_split(args.images, ground_truth, PRESETS[args.preset], args.max_side, IOU_THRESHOLD)
    report = build_report(args.preset, args.split_name, score, args.max_side)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / f"metrics_{args.preset}_{args.split_name}.json").write_text(json.dumps(report, indent=2))
    print(table_row(report))
    log.info("done, %d images skipped", score.images_skipped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
