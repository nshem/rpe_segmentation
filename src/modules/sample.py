from src.modules.photo import Photo
from src.modules.sam import generator


class Sample:
    def __init__(self, _file_name: str):
        self.photo = Photo(_file_name)
        self.masks = self.photo.generate_masks(generator)


def load_sample_return_image(sample: Sample) -> str:
    return sample.photo.to_png_bytes()
