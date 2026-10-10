# Data

## Laboro Tomato (evaluation set, not included)

Download it yourself from the official repository, https://github.com/laboroai/LaboroTomato (direct link: `http://assets.laboro.ai.s3.amazonaws.com/laborotomato/laboro_tomato.zip`, about 1.6 GB), and unzip it so the layout is:

```
data/laboro/laboro_tomato/
├── annotations/train.json   (COCO format, 643 images)
├── annotations/test.json    (COCO format, 161 images)
├── train/*.jpg
└── test/*.jpg
```

Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. Commercial use requires contacting Laboro.AI Inc. The dataset and its images are **not** redistributed in this repository, and `data/laboro/` is git ignored.

The ground truth class used is "fully ripened" (`b_fully_ripened` and `l_fully_ripened`). Half ripened and green fruit count as background.
