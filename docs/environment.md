# Environment and evaluation notes

## Machine
- Windows 11, Python 3.14.4 (the package needs 3.11 or newer; CI uses 3.11).
- `opencv-python-headless` 5.0.0, `numpy` 2.5.3, `matplotlib` 3.11.2, `pytest` 9.1.1.
- `ffmpeg` 8.1.1 (gyan.dev build). Demo video length: 302.9 s.

## Notes
- Two shared evaluation helpers were added as shared code: `eval/scoring.py` (scores one split; used by both `run_eval.py` and `tune.py` so the logic exists once). `sim/plot.py` makes the simulation plot. `ORIGINAL_CONTROL` and a `PRESETS` name table were added to `config/presets.py`.
- The Laboro images are 12 MP (3024 x 4032 or 3120 x 4160). Detection runs on a copy downscaled to a longest side of 640 px and the boxes are scaled back to original pixels before matching. The `min_area_px` values (50, 150, 400) therefore refer to that 640 px working size. The same setting is used for every preset and for tuning.
- The `ORIGINAL` preset flips the image vertically (the robot's camera was mounted upside down). Dataset photos are upright, so in evaluation the returned boxes are mirrored back before matching. Without this the original preset scored 0.034 precision and 0.016 recall on train, which measured the flip, not the detector.

## Source files (read only, copied, never modified)
Root: `C:\Users\Laria\Documents\Ali Docs\Documents\Hamdard\972-2019 Muhammad Ali Lari FYDP\Report Folder\`

| File | Size (bytes) |
|---|---|
| `Programs\Rpi Code.py` | 4339 |
| `Programs\ESP-32 Code.ino` | 2650 |
| `Design and development of IoT based Harvesting Robo Vec\FYDP Report.pdf` | 3502802 (modified 2023-10-01) |
| `...\Images\#1.jpeg` to `#7.jpeg`, `#8.png` | 8 files present |
| `...\Video\Design and Development of Harvesting Robo Vec.mp4` | present, 302.9 s |

Hashes of the two copied code files are recorded in `original/README.md` and match the sources.

## Dataset: Laboro Tomato
- Source: https://github.com/laboroai/LaboroTomato, file `http://assets.laboro.ai.s3.amazonaws.com/laborotomato/laboro_tomato.zip`, 1,645,418,377 bytes (server `Last-Modified` 2020-07-03). Downloaded 2026-10-10.
- Licence (as stated on the repository page): Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (https://creativecommons.org/licenses/by-nc-sa/4.0/); commercial use requires contacting Laboro.AI Inc.
- Format verified: COCO JSON with `bbox` present on every annotation (polygon fallback is implemented and tested but not needed). `annotations/train.json`: 643 images, 7781 annotations. `annotations/test.json`: 161 images, 1996 annotations.
- Categories (6): `b_fully_ripened`, `b_half_ripened`, `b_green`, `l_fully_ripened`, `l_half_ripened`, `l_green`. "Fully ripened" ground truth = `b_fully_ripened` and `l_fully_ripened`.
- Image file names in the JSON are relative to `train/` and `test/`.

## Tuning run
- Full train split (643 images), 54 grid points (3 x 3 x 2 x 3), about 70 minutes on this machine. No subset fallback was needed. Best F1 0.419 on train.

## Media
- `docs/img/demo.gif`: cut from 248 s to 260 s of the demo video (4.6 MB). **Timestamps pending the author's confirmation.**
- `docs/img/robot_side.jpg`, `robot_arm_sensor.jpg`, `robot_electronics.jpg` are photos #5, #7 and #6. **Choice pending the author's confirmation.** None of the eight photos shows a tomato or a camera view, so the overlay images in `docs/img/overlay_frame_*.png` come from frames of the demo video (the target there is a red object, not a tomato).
