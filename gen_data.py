import os
import sys
import json

from tqdm import tqdm
import numpy as np
import cv2


def gen_img(split, data, reweight=0):
    if split == "val":
        reweight = 0
    for key, instance in tqdm(data.items()):
        load_path = instance["path"]

        # label_path: path to store label (txt)
        label_path = load_path[:-3] + "txt"
        label_path = os.path.join(f"{split}_label", label_path)
        label_path = os.path.abspath(label_path)

        # image_path: path to store image (png)
        image_path = os.path.join(f"{split}_image", load_path)[:-3] + "png"
        image_path = os.path.abspath(image_path)

        # load_path: path to load original npy file
        load_path = os.path.join(split, load_path)
        load_path = os.path.abspath(load_path)

        os.makedirs(os.path.dirname(label_path), exist_ok=True)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        coords = instance["coords"]

        with open(label_path, "w") as f:
            # convert to np.uint8 and save the image
            image = np.load(load_path).astype(np.float32)
            image = ((image + 1024) / 4096 * 255).astype(np.uint8)
            image = np.stack([image]*3, axis=-1)
            cv2.imwrite(image_path, image)

            # save normalized bbox
            h, w = image.shape[0], image.shape[1]
            for coord in coords:
                f.write(f"0 {coord[0]/w} {coord[1]/h} {64/w} {64/h}\n")

            # reweight positive samples
            if instance["label"] == 1 and reweight > 0:
                for i in range(reweight-1):
                    os.symlink(image_path, image_path[:-4] + f"_cp{i}.png")
                    os.symlink(label_path, label_path[:-4] + f"_cp{i}.txt")

if __name__ == '__main__':
    try:
        reweight = int(sys.argv[1])
    except:
        reweight = 0

    for split in ["train", "val"]:
        data = json.load(open(f"records_{split}.json", "r"))
        data = data["datainfo"]
        gen_img(split, data, reweight)
