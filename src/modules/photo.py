import cv2, os
import numpy as np
import os
from segment_anything import SamAutomaticMaskGenerator
import cv2
from typing import Dict
import numpy as np
from modules.mask import Mask
import modules.mask as mask_module
import modules.utils as utils
import datetime
import base64
from modules.storage import storage


class Photo(np.ndarray):
    storage_obj: storage.Photo
    id: int
    filename: str

    def __new__(
        self, id: int
    ):  ## using __new__ instead of __init__ because np.ndarray uses it, and we want to inherit from it

        # load photo from db by id
        print(f"Loading photo with id {id}")
        storage_photo = storage.Photo.get_by_id(id)
        if not storage_photo:
            raise FileNotFoundError(f"Photo with id {id} not found")
        print(f"Photo({storage_photo.id}) loaded from db")

        # decode image from db: base64 string to np.ndarray
        _bytes = base64.b64decode(storage_photo.nparray)
        img = np.frombuffer(_bytes, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        # create new instance of np.ndarray
        self = super().__new__(
            self, shape=img.shape, dtype=img.dtype, strides=img.strides, buffer=img
        )

        # set attributes to created instance (note we overrided self^)
        self.storage_obj = storage_photo
        self.id = id
        self.filename = storage_photo.filename

        return self

    @classmethod
    def create_new(cls, _filename: str, _bytes: bytes):
        print(f"creating photo with id {id}")
        try:
            storage_obj = (
                storage.Photo.select().where(storage.Photo.filename == _filename).get()
            )
        except storage.Photo.DoesNotExist:
            storage_obj = storage.Photo.create(
                filename=_filename, nparray=base64.b64encode(_bytes).decode("utf-8")
            )
        return Photo(storage_obj.id)

    @classmethod
    def get_all_ids(cls):
        return [photo.id for photo in storage.Photo.select(storage.Photo.id)]

    def delete(self):
        print(f"deleting photo with id {self.id}")
        return storage.Photo.delete_by_id(self.id)

    def generate_masks(self, mask_generator: SamAutomaticMaskGenerator):
        sam_results = mask_generator.generate(self)
        batch_id = datetime.datetime.now()

        self.delete_masks()

        filtered_results = filter_masks(sam_results, self)
        sorted_masks = mask_module.sort_masks(filtered_results)
        masks = [Mask.create_new(mask, self.id, batch_id) for mask in sorted_masks]

        return masks

    def delete_masks(self):
        try:
            self.storage_obj.delete_masks()
        except Exception as e:
            print(e)
            raise Exception(f"Failed to delete masks for photo with id {self.id}: {e}")

    def get_masks(self) -> list[Mask]:
        return [Mask(mask.id) for mask in self.storage_obj.masks.select()]

    def has_masks(self) -> bool:
        return self.storage_obj.has_masks()

    def is_touching_image_edge(self, mask: dict) -> bool:
        height, width, _ = self.shape
        contours, _ = cv2.findContours(
            mask["segmentation"].astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE,
        )
        for contour in contours:
            for point in contour:
                x, y = point[0]
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    return True
        return False

    def to_png_bytes(self) -> bytes:
        _, buffer = cv2.imencode(".png", self)
        return base64.b64encode(buffer).decode("utf-8")


def filter_masks(masks: list[dict], original_image: Photo) -> list[dict]:
    areas_mean = np.mean([mask["area"] for mask in masks])
    return [
        mask
        for mask in masks
        if not original_image.is_touching_image_edge(mask)
        and not utils.smaller_then_third_mean(mask["area"], areas_mean)
    ]
