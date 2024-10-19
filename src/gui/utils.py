import base64, os, logging
from src.modules.sample import Sample
from src.modules.storage import storage


class SampleData:
    name: str
    b64: str
    id: int
    has_masks: bool = False
    selected: bool = False

    def __init__(self, _id: int, _b64: str, _name: str, _has_masks: bool = False):
        self.b64 = _b64
        self.name = _name
        self.id = _id
        self.has_masks = _has_masks

    def filename(self) -> str:
        return self.name + ".png"


def load_all_samples() -> list[SampleData]:
    samples: list[Sample] = Sample.get_all()
    print(f"Found {len(samples)} samples: {samples}")

    samplesDisplayData: list[SampleData] = []
    for sample in samples:
        print(f"Sample ID: {sample.id}, Photo Name: {sample.photo.filename}")
        samplesDisplayData.append(
            SampleData(
                _b64=sample.photo.to_png_bytes(),
                _name=sample.photo.filename.split(".")[0],
                _id=sample.id,
                _has_masks=sample.has_masks,
            )
        )

    return samplesDisplayData


# def load_from_folder():
#     image_data: list[SampleData] = []
#     try:
#         for file in os.listdir(os.getenv("SAMPLES_PATH", "")):
#             if not file.endswith(".png"):
#                 continue

#             s = Sample(file)
#             img = s.photo.to_png_bytes()
#             image_name = file.split(".")[0]
#             image_data.append(SampleData(_b64=img, _name=image_name))
#     except Exception as e:
#         logging.error(e)
#     return image_data
