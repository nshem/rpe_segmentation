import cv2, os
import numpy as np
import os
from segment_anything import SamAutomaticMaskGenerator
import cv2
from typing import Dict
import numpy as np
import random
import shapely

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
    
class Photo(np.ndarray):
    def __new__(self, _file_name: str):
        self.file_name = _file_name
        img = self._load_image(self, _file_name)        
        return super().__new__(self, shape=img.shape, dtype=img.dtype, strides=img.strides, buffer=img)

    def _load_image(self, image_name: str) -> np.ndarray:
        image_path = os.path.join(".", "data", image_name)
        img = cv2.imread(image_path)
        img = self._preprocess_image(self, img)
        return img
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def generate_masks(self, mask_generator: SamAutomaticMaskGenerator):
        sam_results = mask_generator.generate(self)
        masks = [ Mask(mask) for mask in sam_results ]
        filtered_results = filter_masks(masks, self)
        sorted_masks = sort_masks(filtered_results)

        return sorted_masks

    def is_touching_image_edge(self, mask) -> bool:
        height, width = self.shape[1:]
        contours = mask.contours
        for contour in contours:
            for point in contour:
                x, y = point[0]
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    return True
        return False
    
    
def filter_masks(masks: list[Mask], original_image: Photo) -> list[Mask]:
    areas_mean = np.mean([ mask.area for mask in masks ])
    return [
        mask
        for mask
        in masks
        if not original_image.is_touching_image_edge(mask) and not smaller_then_third_mean(mask, areas_mean)
    ]

def smaller_then_third_mean(mask: Mask, areas_mean: float) -> bool:
    return mask.area < areas_mean / 3


def sort_masks(masks: list[Mask]) -> list[Mask]:
    return [
        mask
        for mask
        in sorted(masks, key=lambda x: x.area, reverse=True)
    ]

class Sample:
    def __init__(self, _file_name: str, mask_generator: SamAutomaticMaskGenerator):
        self.photo = Photo(_file_name)
        self.masks = self.photo.generate_masks(mask_generator)

