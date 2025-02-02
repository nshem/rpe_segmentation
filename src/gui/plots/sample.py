import cv2
import matplotlib
import math
import tornado  # required for WebEgg
import plotly.graph_objects as go
import numpy as np

matplotlib.use("WebAgg")

import matplotlib.pyplot as plt, mpld3
from matplotlib.axes import Axes
from modules.sample import Sample
from modules.mask import Mask
from modules.photo import Photo
from shapely.geometry import Polygon
from gui import utils


def display_grid_of_all_polygons(ax: Axes, masks):
    ax.set_title("polygons")
    # display grid of all masks
    for i in range(len(masks)):
        x, y = masks[i].polygon.exterior.xy
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
        ## draw contours
        annotated = cv2.drawContours(
            image=img, contours=[contour], contourIdx=0, color=mask.color, thickness=2
        )

        ## contour mask id for readability
        annotated = cv2.putText(
            img=annotated,
            text=f"{mask.id}",
            org=(
                int(mask.center_coord.x) - len(str(mask.id)) * 5,
                int(mask.center_coord.y) - 8,
            ),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=1,
            thickness=5,
            color=utils.contour_color(mask.color),
        )
        # annotate mask id
        annotated = cv2.putText(
            img=annotated,
            text=f"{mask.id}",
            org=(
                int(mask.center_coord.x) - len(str(mask.id)) * 5,
                int(mask.center_coord.y) - 8,
            ),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=1,
            thickness=2,
            color=mask.color,
        )
        annotated = cv2.circle(
            img=annotated,
            center=(
                int(mask.center_coord.x),
                int(mask.center_coord.y),
            ),
            radius=2,
            color=mask.color,
            thickness=4,
        )

    ax.imshow(annotated)


def display_grid_of_all_slider(img, masks):
    # Create a figure
    fig = go.Figure()

    # Add the original image as the background
    fig.add_trace(go.Image(z=img))

    # Create annotated images with contours and slider steps
    steps = []
    for i, mask in enumerate(masks):
        # Draw the contour
        contour = max(mask.contours, key=cv2.contourArea)
        annotated_img = img.copy()
        annotated_img = cv2.drawContours(
            image=annotated_img, contours=[contour], contourIdx=0, color=mask.color, thickness=2
        )

        # Add each annotated image as a separate trace
        fig.add_trace(go.Image(z=annotated_img, visible=False if i > 0 else True))

        # Create a slider step
        step = dict(
            method='update',
            args=[{'visible': [j == i for j in range(len(masks))]}],  # Toggle visibility
            label=mask.id,
        )
        steps.append(step)

    # Create the slider
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Mask ID: "},
        pad={"t": 50},
        steps=steps,
    )]

    fig.update_layout(sliders=sliders,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    return fig


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

    # Generate the Plotly figure with the slider
    plotly_fig = display_grid_of_all_slider(sample.photo, sample.masks)
    plotly_fig.show('browser')

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
