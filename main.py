import os
import subprocess
import torch
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import cv2
import supervision as sv
from typing import Dict
import numpy as np
import matplotlib.pyplot as plt
import random


# source:
# https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-segment-anything-with-sam.ipynb

# setup the environment
# chmod +x ./setup.sh
subprocess.check_output("./setup.sh", shell=True).decode("utf-8")
HERE = "."
# make sure the weights are downloaded
CHECKPOINT_PATH = os.path.join(HERE, "weights", "sam_vit_h_4b8939.pth")
print(CHECKPOINT_PATH, "; exist:", os.path.isfile(CHECKPOINT_PATH))

# load the model
DEVICE = torch.device("cpu") # or cuda/cpu if not mac
MODEL_TYPE = "vit_h"
sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)


# mask generator
mask_generator = SamAutomaticMaskGenerator(sam)

# load the image

IMAGE_NAME = "5G.png"
IMAGE_PATH = os.path.join(HERE, "data", IMAGE_NAME)

# generate the mask
image_bgr = cv2.imread(IMAGE_PATH)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

sam_result = mask_generator.generate(image_rgb)

# output the mask
print(sam_result[0].keys())
# mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX)
# detections = sv.Detections.from_sam(sam_result=sam_result)
# annotated_image = mask_annotator.annotate(scene=image_bgr.copy(), detections=detections)

# display the results on the image
# sv.plot_images_grid(
#     images=[image_bgr, annotated_image],
#     grid_size=(1, 2),
#     titles=['source image', 'segmented image']
# )

height, width = image_bgr.shape[1:]

def is_touching_image_edge(mask: Dict[str, any], height: int, width: int) -> bool:
    np_mask = mask['segmentation'].astype(np.uint8)
    contours, _ = cv2.findContours(np_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        for point in contour:
            x, y = point[0]
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                return True
    return False

# filter out masks that are touching the image edge
filtered_results = [mask for mask in sam_result if not is_touching_image_edge(mask, height, width)]

print(len(sam_result), len(filtered_results))
masks = [
    mask['segmentation']
    for mask
    in sorted(filtered_results, key=lambda x: x['area'], reverse=True)
]

def polygon_from_mask(mask: np.ndarray) -> cv2.typing.MatLike:
    mask = mask.astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key = cv2.contourArea)
    epsilon = 0.025 * cv2.arcLength(contour, True)
    aprox = cv2.approxPolyDP(contour, epsilon, True)
    img = image_bgr
    poly = cv2.drawContours(image=img, contours=[aprox], contourIdx=0, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), thickness=3)

    return poly

polygons = [polygon_from_mask(mask) for mask in masks]
# for polygon in polygons:
plt.imshow(polygons[0], interpolation='nearest')
plt.show()

# shapely.plotting.plot_polygon(polygons[0])


# display grid of all masks
# sv.plot_images_grid(
#     images=polygons,
#     grid_size=(8, int(len(masks) / 8) + 1),
#     size=(16, 16)
# )


print("done")