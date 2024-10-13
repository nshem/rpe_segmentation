from src.modules.photo import Photo
from src.modules.mask import Mask
from src.modules.sam import generator


class Sample:
    def __init__(self, id: int):
        self.photo = Photo(id)
        ## load masks from db
        self.masks: list[Mask] = []

    def generate_masks(self):
        self.masks = self.photo.generate_masks(generator)


def load_sample_return_image(sample: Sample) -> str:
    return sample.photo.to_png_bytes()
