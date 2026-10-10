# Observations about the original code

Stated neutrally: it is a student project that worked on the robot. "Addressed in v2" refers to the rebuild in `tomato_vision/`.

| # | Observation | Where | Addressed in v2 |
|---|---|---|---|
| 1 | One hue range, 0 to 14. Reds near hue 179 (the other side of the hue wrap) are missed | `lower_red`, `upper_red` | yes (two ranges, tested with hue 175) |
| 2 | Morphological cleanup is commented out, so speckle stays in the mask | mask section | yes (open and close, configurable) |
| 3 | No minimum area, so a tiny blob can become the target | `max(contours)` | yes (`min_area_px`) |
| 4 | `requests.get` without a timeout: an unresponsive vehicle freezes the loop | all command sends | yes (`urlopen` with a timeout, STOP on failure) |
| 5 | The result of `cap.read()` is not checked; a failed read crashes at `cv2.flip` | main loop | yes (a failed read stops the robot and exits non zero) |
| 6 | Targets above and below the band both send `f` (advance) | y branch | no (kept on purpose; noted as `ADVANCE`) |
| 7 | `l` is sent for a target on the right and `r` for the left | x branch | no (kept; tied to the vehicle wiring and the flipped camera) |
| 8 | Arm firmware uses blocking `delay()` (1.5 s and 2 s) and fixed width serial parsing (`substring(2,5)`), so numbers must be zero padded to 3 digits | `.ino` | partly (the protocol module always pads; the firmware is not rebuilt) |
| 9 | Distance assumes a 4 cm object and a 520 px focal length | distance line | no (same formula, constants configurable) |
| 10 | Vision script speaks HTTP, arm firmware speaks serial, the joining code is not in the archive | whole system | n/a |
| 11 | The arm angles are an open loop `map()` to hobby servos; only the vehicle alignment uses camera feedback | `.ino` | n/a (described as vision guided alignment) |
