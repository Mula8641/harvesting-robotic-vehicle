import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Box:
    x1: float
    y1: float
    x2: float
    y2: float


def _polygon_extent(segmentation: list[list[float]]) -> Box:
    xs = [value for polygon in segmentation for value in polygon[0::2]]
    ys = [value for polygon in segmentation for value in polygon[1::2]]
    return Box(min(xs), min(ys), max(xs), max(ys))


def _annotation_box(annotation: dict) -> Box:
    if "bbox" in annotation:
        x, y, width, height = annotation["bbox"]
        return Box(x, y, x + width, y + height)
    return _polygon_extent(annotation["segmentation"])


def load_ground_truth(annotations_path: Path, class_names: frozenset[str]) -> dict[str, list[Box]]:
    with open(annotations_path, encoding="utf-8") as handle:
        data = json.load(handle)
    category_ids = {c["id"] for c in data["categories"] if c["name"] in class_names}
    if not category_ids:
        available = sorted(c["name"] for c in data["categories"])
        raise KeyError(f"none of {sorted(class_names)} in categories {available}")
    boxes = {image["file_name"]: [] for image in data["images"]}
    names_by_id = {image["id"]: image["file_name"] for image in data["images"]}
    for annotation in data["annotations"]:
        if annotation["category_id"] in category_ids:
            boxes[names_by_id[annotation["image_id"]]].append(_annotation_box(annotation))
    return boxes
