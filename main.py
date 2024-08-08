import os
import subprocess
import torch
from segment_anything import modeling, sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import cv2
import supervision as sv
from typing import Dict
import random
import matplotlib.pyplot as plt
from matplotlib import transforms
import matplotlib.axes as Axes
from dotenv import load_dotenv
from photo import Sample, Photo, Mask

CHECKPOINT_PATH = os.path.join(".", "weights", "sam_vit_h_4b8939.pth")

# setup the environment
# chmod +x ./setup.sh
def setup():
    load_dotenv()

    subprocess.check_output("./setup.sh", shell=True).decode("utf-8")
    # make sure the weights are downloaded
    print(CHECKPOINT_PATH, "; weights exist:", os.path.isfile(CHECKPOINT_PATH))
    print("setup done")


def init_sam() -> modeling.Sam:
    DEVICE = torch.device("cpu") # or cuda/cpu if not mac
    MODEL_TYPE = "vit_h"
    return sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)


def init_mask_generator() -> SamAutomaticMaskGenerator:
    sam = init_sam()
    return SamAutomaticMaskGenerator(sam)


def display_grid_of_all_polygons(ax: Axes, masks):
    ax.axis('off')
    ax.set_title("polygons")
    # display grid of all masks
    for i in range(len(masks)):
        x, y = masks[i].polygon.exterior.xy
        # rot = transforms.Affine2D().rotate_deg(90)
        ax.plot(x, y, linewidth=1, color=(masks[i].color[0] / 255, masks[i].color[1] / 255, masks[i].color[2] / 255))
        ax.yaxis.set_inverted(True)
        ax.set_aspect('equal')


def display_grid_of_all(ax: Axes, img, masks):
    ax.set_title("segmentation")
    ax.axis('off')
    for mask in masks:
        contour = max(mask.contours, key = cv2.contourArea)
        annotated = cv2.drawContours(image=img, contours=[contour], contourIdx=0, color=mask.color, thickness=2)
    ax.imshow(annotated)

def corners_number_dist(ax, polygons):
    corners = [len(p.exterior.coords) - 1 for p in polygons]
    ax.hist(corners, bins=range(2, 12, 1), label="corners number")
    ax.set_title("corners number dist")

def area_dist(ax, polygons):
    areas = [p.area for p in polygons]
    ax.hist(areas, bins=range(0, int(max(areas)), 100), label="area dist")
    ax.set_title("area dist")

def average_angle_dist(ax, masks):
    angles = [m.average_angle_per_polygon() for m in masks]
    ax.hist(angles, bins=range(0, 180, 10), label="angle dist")
    ax.set_title("largest angle diff dist")

def main():
    setup()
    mask_generator = init_mask_generator()
    sample = Sample(f"1.png", mask_generator)
    polygons = [mask.polygon for mask in sample.masks]
    fig, axs = plt.subplot_mosaic([['A', 'A', 'B', 'B'],['A', 'A', 'B', 'B'], ['C', 'D', 'E', 'H']])
    display_grid_of_all_polygons(axs['A'], sample.masks)
    display_grid_of_all(axs['B'], sample.photo, sample.masks)
    corners_number_dist(axs['C'], polygons)
    area_dist(axs['D'], polygons)
    average_angle_dist(axs["E"], sample.masks)

    axs['H'].axis('off')
    axs["H"].text(0, 0, f"polygons: {len(polygons)}")

    plt.show()

main()