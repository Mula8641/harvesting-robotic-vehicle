import argparse
import dataclasses
import itertools
import json
import random
import sys
from pathlib import Path

from tomato_vision.config.presets import ADVANCED
from tomato_vision.config.settings import DetectorConfig, HsvRange
from tomato_vision.eval.coco_loader import load_ground_truth
from tomato_vision.eval.metrics import precision_recall_f1
from tomato_vision.eval.run_eval import IOU_THRESHOLD, RIPE_CLASSES
from tomato_vision.eval.scoring import score_split
from tomato_vision.utils.log import get_logger

HUE_UPPER = (10, 14, 18)
SAT_MIN = (47, 80, 120)
VAL_MIN = (40, 60)
MIN_AREA = (50, 150, 400)
SEED = 0

log = get_logger(__name__)


def candidate_config(hue_upper: int, sat_min: int, val_min: int, min_area: int) -> DetectorConfig:
    ranges = (
        HsvRange((0, sat_min, val_min), (hue_upper, 255, 255)),
        HsvRange((179 - hue_upper, sat_min, val_min), (179, 255, 255)),
    )
    return dataclasses.replace(ADVANCED, hue_ranges=ranges, min_area_px=min_area)


def run_grid(images_dir: Path, ground_truth: dict, max_side: int) -> list[dict]:
    grid = []
    for hue_upper, sat_min, val_min, min_area in itertools.product(HUE_UPPER, SAT_MIN, VAL_MIN, MIN_AREA):
        config = candidate_config(hue_upper, sat_min, val_min, min_area)
        score = score_split(images_dir, ground_truth, config, max_side, IOU_THRESHOLD)
        precision, recall, f1 = precision_recall_f1(score.tp, score.fp, score.fn)
        grid.append({"hue_upper": hue_upper, "sat_min": sat_min, "val_min": val_min, "min_area_px": min_area,
                     "tp": score.tp, "fp": score.fp, "fn": score.fn,
                     "precision": precision, "recall": recall, "f1": f1})
        log.info("%s", grid[-1])
    return grid


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--split-name", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-side", type=int, default=640)
    parser.add_argument("--subset", type=int, default=0, help="random subset size, 0 means all")
    args = parser.parse_args(argv)
    if args.split_name == "test":
        log.error("tuning on the test split is not allowed")
        return 2
    ground_truth = load_ground_truth(args.annotations, RIPE_CLASSES)
    if args.subset:
        names = random.Random(SEED).sample(sorted(ground_truth), min(args.subset, len(ground_truth)))
        ground_truth = {name: ground_truth[name] for name in names}
    grid = run_grid(args.images, ground_truth, args.max_side)
    best = max(grid, key=lambda row: row["f1"])
    args.out.mkdir(parents=True, exist_ok=True)
    result = {"split": args.split_name, "seed": SEED, "subset": args.subset, "max_side_px": args.max_side,
              "images": len(ground_truth), "best": best, "grid": grid}
    (args.out / "tuning_train.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(best))
    return 0


if __name__ == "__main__":
    sys.exit(main())
