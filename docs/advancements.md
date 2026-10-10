# From the 2023 project to later work

The 2023 code ran on the robot and produced the results in my final year report. This page lists what the later work in `tomato_vision/` adds on top of it, and what it deliberately keeps. The 2023 files stay as they were in [`original/`](../original/README.md).

| Area | 2023 project | Later work (`tomato_vision/`) |
|---|---|---|
| Red range | one hue range, 0 to 14 | two ranges so reds near hue 179 are also found; bounds chosen on a public dataset |
| Mask cleanup | not applied | morphological open and close, configurable |
| Small blobs | the largest contour is the target | a minimum area filter; all candidates are reported |
| Vehicle link | HTTP GET with the default behaviour | a timeout, and a STOP when the vehicle or camera fails |
| Camera read | frame used as read | a failed read stops the loop with a clear error |
| Structure | one script with one loop | small modules with tests, a `--dry-run` mode that needs no robot |
| Evaluation | trial counts on the physical robot (see the report) | a reproducible test on the public Laboro Tomato dataset |
| Alignment | closed loop on the vehicle, measured on the robot | the same decision table, plus a simulation of the loop |
| Arm firmware | `.ino` with `map()` ranges | the same ranges as a tested Python model and serial frame builders (the firmware itself is unchanged) |

## Observation about the archived 2023 script
In `rpi_vision_original.py` the edge trigger flag `a` is reset to 0 in the x centred branch before the y branch runs. The pick branch (`sa`) only executes when `a == 1`, so it cannot be reached. A target centred in x but outside the y band also makes the script send `f`, then `s`, then `f`, alternating every frame. Both were confirmed by running the script's decision logic over all sequences of seven frames drawn from four target positions (right, left, above, centred): no sequence sends `sa`. The robot picked in my trials, so the version used on the robot, or how the pick was started, may differ from this file (an earlier copy, `Pi_Code.py` dated 07.07.2023, exists on my Drive and has not been compared). The later work sends PICK when the target is inside the dead band on both axes, which is the evident intent.

## Kept as in 2023
- The `l` and `r` command mapping (tied to the vehicle wiring and the flipped camera).
- One shared `f` command for a target above or below the centre band.
- The 40 px dead band, the 255 x 255 frame, the 4 cm object and 520 px focal length assumption for distance.

## Not in the archive
- The code that joins the vision script (HTTP) to the arm firmware (serial).
- The obstacle avoidance code for the ultrasonic sensor.
