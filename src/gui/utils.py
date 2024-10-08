import base64, os, logging
from src.modules.sample import Sample
from src.modules.storage import storage


class ImageData:
    name: str
    b64: str
    id: int

    def __init__(self, _id: int, _b64: str, _name: str):
        self.b64 = _b64
        self.name = _name
        self.id = _id

    def filename(self) -> str:
        return self.name + ".png"


def load_images() -> list[ImageData]:
    storage_photos: list[storage.Photo] = storage.Photo.select()

    samples: list[ImageData] = []
    for photo in storage_photos:
        sample = Sample(int(photo.id))
        samples.append(
            ImageData(
                _b64=sample.photo.to_png_bytes(),
                _name=sample.photo.filename.split(".")[0],
                _id=photo.id,
            )
        )

    return samples


def load_from_folder():
    image_data: list[ImageData] = []
    try:
        for file in os.listdir(os.getenv("SAMPLES_PATH", "")):
            if not file.endswith(".png"):
                continue

            s = Sample(file)
            img = s.photo.to_png_bytes()
            image_name = file.split(".")[0]
            image_data.append(ImageData(_b64=img, _name=image_name))
    except Exception as e:
        logging.error(e)
    return image_data
