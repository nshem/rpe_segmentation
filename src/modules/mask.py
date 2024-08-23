import cv2, os
import numpy as np
import os
from segment_anything import SamAutomaticMaskGenerator
import cv2
from typing import Dict
import numpy as np
import random
import shapely
import src.modules.utils as utils

class Mask:
    def __init__(self, _mask: Dict[str, any]):
        self.segmentation = _mask['segmentation']
        self.area = _mask['area']
        self.predicted_iou = _mask['predicted_iou']
        self.point_coords = _mask['point_coords']
        self.stability_score = _mask['stability_score']
        self.crop_box = _mask['crop_box']
        self.bbox = _mask['bbox']
        self.original_dict = _mask
        ctrs, _ = cv2.findContours(self.segmentation.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.contours = ctrs
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.polygon = self._polygon_from_mask()

    def _polygon_from_mask(self) -> cv2.typing.MatLike:
        contours = self.contours
        contour = max(contours, key = cv2.contourArea)
        epsilon = 0.04 * cv2.arcLength(contour, True)
        aprox = cv2.approxPolyDP(contour, epsilon, True)

        p = [a[0] for a in aprox]
        polygon = shapely.Polygon(p)

        return polygon

    def average_angle_per_polygon(self) -> float:
        coords = self.polygon.exterior.coords[1:]
        return np.max(np.diff([utils.calculate_angle(coords, i) for i in range(len(coords) - 1)]))
    

def sort_masks(masks: list[Mask]) -> list[Mask]:
    return [
        mask
        for mask
        in sorted(masks, key=lambda x: x.area, reverse=True)
    ]
