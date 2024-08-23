import cv2, os
import numpy as np
import os
from segment_anything import SamAutomaticMaskGenerator
import cv2
from typing import Dict
import numpy as np
from src.modules.mask import Mask
import src.modules.mask as mask_module
import src.modules.utils as utils

class Photo(np.ndarray):
    def __new__(self, _file_name: str):
        self.file_name = _file_name
        img = self._load_image(self, _file_name)        
        return super().__new__(self, shape=img.shape, dtype=img.dtype, strides=img.strides, buffer=img)

    def _load_image(self, image_name: str) -> np.ndarray:
        image_path = os.path.join(".", "data", image_name)
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"File {image_path} not found")
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
        sorted_masks = mask_module.sort_masks(filtered_results)

        return sorted_masks

    def is_touching_image_edge(self, mask) -> bool:
        height, width, _ = self.shape
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
        if not original_image.is_touching_image_edge(mask) and not utils.smaller_then_third_mean(mask.area, areas_mean)
    ]
