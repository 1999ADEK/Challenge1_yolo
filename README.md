# Challenge1_yolo

- yolov5: https://github.com/ultralytics/yolov5.git
- To generate dataset for yolov5, please refer to [gen_data.py](gen_data.py).
  Do note that it is somewhat hard-coded and is expected to be put under DEEP01_NTUEE_DLCV_2021_train/. Below is the usage:
  ```
  python gen_data.py [weight]
  ```
  where `[weight]` can be used to balance positive and negative cases in the dataset. The number of positive cases will be multiplied by this ‵[weight]`.
- One can follow the instruction [here](https://docs.ultralytics.com/tutorials/train-custom-datasets/) to train yolov5 on custom datasets.
  Basically a yaml file should be created and put under yolov5/data/ to specify the paths to your dataset.
- My baseline model:
  - Generate data with `python gen_data.py 4`.
  - In yolov5, simply run `python train.py --data data/my_data.yaml --img 512`
