# Original code (unmodified)

Two files from my final year project (B.E. Electrical Engineering, Hamdard University, Karachi, 2023). They are byte identical copies of the files in my project archive and have not been edited.

| File | Source in the archive | What it is |
|---|---|---|
| `rpi_vision_original.py` | `Report Folder\Programs\Rpi Code.py` | Raspberry Pi vision script |
| `esp32_arm_original.ino` | `Report Folder\Programs\ESP-32 Code.ino` | ESP32 arm firmware |

SHA-256 of the copies:
- `rpi_vision_original.py`: `FB563D8ED4B814A5249C754E69010F852638BADA593A545C4487D24584498397`
- `esp32_arm_original.ino`: `71FE643432E7EADD7B8C227EDA603722AE9EF79F247F094C1C86E81E00172505`

## What they do

`rpi_vision_original.py` (about 155 lines, one infinite loop) reads a 255 x 255 camera frame, flips it vertically, raises the brightness by 50 and thresholds it in HSV with one red range (`(0,47,40)` to `(14,255,255)`). It keeps the largest contour, draws its bounding box, estimates distance as `4 * 520 / box_width` (a 4 cm object and a 520 px focal length are assumed) and chooses a command from the box centre: `l` if the centre is more than 40 px right of the frame centre, `r` if more than 40 px left, `f` if centred in x but outside the 40 px band in y, `s` to stop and `sa` when centred in both (the pick trigger). The command is sent by HTTP GET to `http://192.168.4.1/?State=<code>` and only when the state changes.

`esp32_arm_original.ino` (about 100 lines) drives 5 servos (GPIO 16, 17, 5, 18, 19: base, shoulder, elbow, wrist, gripper). It reads serial lines: `T,xxx,yyy` maps x and y (0..255) to base, shoulder and elbow angles; `P,...,zzz` maps z to the wrist angle, closes the gripper, lifts the arm and resets, with blocking `delay()` calls.

## Gaps

- The vision script talks **HTTP** to a vehicle controller that is not in the archive. The arm firmware listens on **serial**. The code that joins the two is not in the archive.
- The obstacle avoidance code (ultrasonic sensor) is **not in the archive**.
- An earlier copy of the vision script (`Pi_Code.py`, 07.07.2023) exists on my shared Drive. It was not compared with this file; if it differs, the difference will be recorded here.
