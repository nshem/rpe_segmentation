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

from dataclasses import dataclass


class Mask:
    storage_obj: storage.Mask
    id: int
    photo_id: int

    segmentation: np.ndarray
    area: float
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
        self.photo_id = _mask.photo_id
        self.id = _id

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
    return [mask for mask in sorted(masks, key=lambda x: x["area"], reverse=True)]


# Define the class with type annotations
class MaskData:

    def __init__(
        self,
        segmentation: Union[Dict[str, Any], np.ndarray],
        bbox: List[float],
        area: float,
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


@dataclass
class Coordinate:
    x: float
    y: float

    def __init__(self, l: list[float]):
        self.x = l[0]
        self.y = l[1]

    def __str__(self):
        return f"({self.x}, {self.y})"


@dataclass
class MaskReport:
    sample_id: str
    mask_id: str
    area: float
    perimeter_length: float
    coordinates: list[Coordinate]  # on the original image
    centroid: Coordinate
    focal_length: float
    roundness: float  # area of the best fitting circle to the area of the mask
    polygon_coordinates: list[Coordinate]  # on the original image
    polygon_corners: int
    polygon_resemblance: (
        float  # between 0-1 - how much the polygon resembles the original mask
    )

    def __init__(self, mask: Mask):
        self.sample_id = mask.photo_id
        self.mask_id = mask.id
        self.area = mask.area
        self.coordinates = [Coordinate(coord) for coord in mask.point_coords]
        self.perimeter_length = utils.calculate_perimiter_length(mask.point_coords)
        self.centroid = Coordinate(utils.calc_centroid(mask.point_coords))
        self.focal_length = utils.calculate_focal_length(mask.point_coords)
        # self.roundness = mask.roundness
        self.polygon_coordinates = [
            Coordinate(coord) for coord in mask.polygon.exterior.coords
        ]
        self.polygon_corners = len(mask.polygon.exterior.coords) - 1
        # self.polygon_resemblance = mask.polygon_resemblance

    def for_gui(self) -> tuple[list[str], list[str]]:
        attributes = []
        values = []
        for attribute, value in self.__dict__.items():
            attributes.append(attribute)
            values.append(str(value))

        return attributes, values

    def to_csv_row(self) -> str:
        return f"{self.sample_id},{self.mask_id},{self.area},{self.perimeter_length},{self.centroid},{self.focal_length},{self.polygon_corners}\n"

    def to_array(self) -> list:
        return [
            self.sample_id,
            self.mask_id,
            self.area,
            self.perimeter_length,
            self.centroid.__str__(),
            self.focal_length,
            self.polygon_corners,
        ]

    def to_csv_header() -> str:
        return "sample_id,mask_id,area,perimeter_length,centroid,focal_length,polygon_corners\n"
