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
import base64
from src.modules.storage import storage


class Photo(np.ndarray):
    id: int
    filename: str

    def __new__(self, id: int):
        photo = storage.Photo.get_by_id(id)
        if not photo:
            raise FileNotFoundError(f"Photo with id {id} not found")
        print(f"Photo({photo.id}) loaded from db")

        self.id = id
        self.filename = photo.filename

        _bytes = base64.b64decode(photo.nparray)
        img = np.frombuffer(_bytes, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        return super().__new__(
            self, shape=img.shape, dtype=img.dtype, strides=img.strides, buffer=img
        )

    @classmethod
    def create_new(cls, _filename: str, _bytes: bytes):
        try:
            storage_obj = (
                storage.Photo.select().where(storage.Photo.filename == _filename).get()
            )
        except storage.Photo.DoesNotExist:
            storage_obj = storage.Photo.create(
                filename=_filename, nparray=base64.b64encode(_bytes).decode("utf-8")
            )

        return Photo(storage_obj.id)

    def delete(self):
        print(f"deleting photo with id {self.id}")
        return storage.Photo.delete_by_id(self.id)

    def generate_masks(self, mask_generator: SamAutomaticMaskGenerator):
        sam_results = mask_generator.generate(self)
        masks = [Mask(mask) for mask in sam_results]
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

    def to_png_bytes(self) -> bytes:
        _, buffer = cv2.imencode(".png", self)
        return base64.b64encode(buffer).decode("utf-8")


def filter_masks(masks: list[Mask], original_image: Photo) -> list[Mask]:
    areas_mean = np.mean([mask.area for mask in masks])
    return [
        mask
        for mask in masks
        if not original_image.is_touching_image_edge(mask)
        and not utils.smaller_then_third_mean(mask.area, areas_mean)
    ]
