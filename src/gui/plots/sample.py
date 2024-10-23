import cv2
import matplotlib
import math
import tornado  # required for WebEgg

matplotlib.use("WebAgg")

import matplotlib.pyplot as plt, mpld3
from matplotlib.axes import Axes
from src.modules.sample import Sample
from src.modules.mask import Mask
from src.modules.photo import Photo
from shapely.geometry import Polygon


def display_grid_of_all_polygons(ax: Axes, masks):
    ax.set_title("polygons")
    # display grid of all masks
    for i in range(len(masks)):
        x, y = masks[i].polygon.exterior.xy
        # rot = transforms.Affine2D().rotate_deg(90)
        ax.plot(
            x,
            y,
            linewidth=1,
            color=(
                masks[i].color[0] / 255,
                masks[i].color[1] / 255,
                masks[i].color[2] / 255,
            ),
        )
        ax.yaxis.set_inverted(True)
        ax.set_aspect("equal")


def display_grid_of_all(ax: Axes, img: Photo, masks: list[Mask]):
    ax.set_title("segmentation")
    ax.axis(False)
    for mask in masks:
        contour = max(mask.contours, key=cv2.contourArea)
        annotated = cv2.drawContours(
            image=img, contours=[contour], contourIdx=0, color=mask.color, thickness=2
        )
    ax.imshow(annotated)


def corners_number_dist(ax: Axes, polygons):
    corners = [len(p.exterior.coords) - 1 for p in polygons]
    ax.hist(corners, bins=range(2, 12, 1), label="corners number")
    ax.set_title("corners number dist")


def area_dist(ax: Axes, polygons: list[Polygon]):
    areas = [p.area for p in polygons]
    maxArea = int(max(areas))
    ax.hist(
        areas,
        range=(0, maxArea),
        label="area dist",
    )
    ax.set_title("area dist")


def average_angle_dist(ax: Axes, masks: list[Mask]):
    angles = [m.average_angle_per_polygon() for m in masks]
    ax.hist(angles, bins=range(0, 180, 10), label="angle dist")
    ax.set_title("largest angle diff dist")


def plot_sample(sample: Sample) -> str:
    polygons = [mask.polygon for mask in sample.masks]

    fig, axs = plt.subplot_mosaic(
        [["A", "A", "B", "B"], ["A", "A", "B", "B"], ["C", "D", "E", "H"]],
        figsize=(10, 10),
    )
    display_grid_of_all_polygons(axs["A"], sample.masks)
    display_grid_of_all(axs["B"], sample.photo, sample.masks)
    corners_number_dist(axs["C"], polygons)
    area_dist(axs["D"], polygons)
    average_angle_dist(axs["E"], sample.masks)
    axs["H"].axis(False)
    axs["H"].text(0, 0, f"polygons: {len(polygons)}")

    return mpld3.fig_to_html(
        fig,
        d3_url=None,
        mpld3_url=None,
        template_type="general",
        figid=None,
        no_extras=False,
        use_http=False,
    )
