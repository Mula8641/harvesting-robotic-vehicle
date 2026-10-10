import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tomato_vision.config.presets import ORIGINAL_CONTROL
from tomato_vision.sim.alignment_sim import simulate_alignment

START_POINTS = {"far right, below": (250.0, 230.0), "far left, above": (5.0, 10.0), "right, centred in y": (200.0, 127.0)}


def main(out_path: Path) -> None:
    fig, (ax_x, ax_y) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
    half_w, half_h = ORIGINAL_CONTROL.frame_width_px / 2, ORIGINAL_CONTROL.frame_height_px / 2
    for label, start in START_POINTS.items():
        steps = simulate_alignment(start, ORIGINAL_CONTROL, 5.0, 200)
        ticks = [s.tick for s in steps]
        ax_x.plot(ticks, [s.target_center_px[0] - half_w for s in steps], label=label)
        ax_y.plot(ticks, [s.target_center_px[1] - half_h for s in steps])
    for ax, name in ((ax_x, "x error (px)"), (ax_y, "y error (px)")):
        ax.axhspan(-ORIGINAL_CONTROL.deadband_px, ORIGINAL_CONTROL.deadband_px, color="grey", alpha=0.2)
        ax.set_ylabel(name)
    ax_y.set_xlabel("tick")
    ax_x.legend()
    ax_x.set_title("Alignment loop: SIMULATION (5 px per tick), grey band = 40 px dead band")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
