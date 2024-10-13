import cv2, os
import numpy as np
import os
import json
import cv2
from typing import Dict
from src.modules.storage import storage
import numpy as np
import random
import shapely
import src.modules.utils as utils
import json
import numpy as np
from typing import Any, Dict, List, Union
import datetime


class Mask:
    storage_obj: storage.Mask
    id: int

    segmentation: np.ndarray
    area: int
    predicted_iou: float
    point_coords: List[List[float]]
    stability_score: float
    crop_box: List[float]
    bbox: List[float]

    color: List[int]
    contours: List[np.ndarray]
    polygon: shapely.geometry.Polygon

    def __init__(self, _id: int):
        print(f"Loading mask with id {_id}")
        _mask: storage.Mask = storage.Mask.get_by_id(_id)
        self.storage_obj = _mask

        try:
            original_dict = string_to_class(_mask.original_dict)
            self.segmentation = original_dict.segmentation
            self.area = original_dict.area
            self.predicted_iou = original_dict.predicted_iou
            self.point_coords = original_dict.point_coords
            self.stability_score = original_dict.stability_score
            self.crop_box = original_dict.crop_box
            self.bbox = original_dict.bbox
        except Exception as e:
            print(e)
            raise Exception(f"Failed to load mask with id {_id}: {e}")

        self.color = json.loads(_mask.color)

        ctrs, _ = cv2.findContours(
            self.segmentation.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        self.contours = ctrs
        self.polygon = self._polygon_from_mask()

    @classmethod
    def create_new(
        self, _mask: Dict[str, any], _photo_id: int, _batch_id: datetime.datetime
    ):
        print(f"Creating new mask for photo with id {_photo_id}")

        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        storage_mask: storage.Mask = storage.Mask.create(
            original_dict=dict_to_string(_mask),
            photo_id=_photo_id,
            color=json.dumps(color),
            batch_id=_batch_id,
        )

        return Mask(storage_mask.id)

    def _polygon_from_mask(self) -> cv2.typing.MatLike:
        contours = self.contours
        contour = max(contours, key=cv2.contourArea)
        epsilon = 0.04 * cv2.arcLength(contour, True)
        aprox = cv2.approxPolyDP(contour, epsilon, True)

        p = [a[0] for a in aprox]
        polygon = shapely.Polygon(p)

        return polygon

    def average_angle_per_polygon(self) -> float:
        coords = self.polygon.exterior.coords[1:]
        return np.max(
            np.diff([utils.calculate_angle(coords, i) for i in range(len(coords) - 1)])
        )


def sort_masks(masks: list[Mask]) -> list[Mask]:
    return [mask for mask in sorted(masks, key=lambda x: x.area, reverse=True)]


# Define the class with type annotations
class MaskData:
    def __init__(
        self,
        segmentation: Union[Dict[str, Any], np.ndarray],
        bbox: List[float],
        area: int,
        predicted_iou: float,
        point_coords: List[List[float]],
        stability_score: float,
        crop_box: List[float],
    ):
        self.segmentation = segmentation
        self.bbox = bbox
        self.area = area
        self.predicted_iou = predicted_iou
        self.point_coords = point_coords
        self.stability_score = stability_score
        self.crop_box = crop_box

    def __repr__(self) -> str:
        return (
            f"MaskData(segmentation={self.segmentation}, bbox={self.bbox}, area={self.area}, "
            f"predicted_iou={self.predicted_iou}, point_coords={self.point_coords}, "
            f"stability_score={self.stability_score}, crop_box={self.crop_box})"
        )


# Function to convert dict to JSON string with type annotations
def dict_to_string(data_dict: Dict[str, Any]) -> str:
    # Handling np.ndarray to ensure it can be converted to JSON
    if isinstance(data_dict["segmentation"], np.ndarray):
        data_dict["segmentation"] = data_dict["segmentation"].tolist()

    return json.dumps(data_dict)


# Function to convert string back to class instance with type annotations
def string_to_class(data_string: str) -> MaskData:
    data_dict = json.loads(data_string)

    # Handling np.ndarray conversion back from list if needed
    if isinstance(data_dict["segmentation"], list):
        data_dict["segmentation"] = np.array(data_dict["segmentation"])

    # Create an instance of MaskData from the dictionary
    return MaskData(**data_dict)
