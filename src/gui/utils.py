import base64, os, logging
from modules.sample import Sample
from modules.storage import storage

from fasthtml.common import *


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


async def extract_sample_ids_from_request(request: Request) -> list[int]:
    form = await request.form()
    sample_ids = [int(sample_id) for sample_id in form.getlist("samples")]
    if len(sample_ids) == 0:
        raise Exception("No samples selected")
    return sample_ids


def set_action_target(context: dict, sample_ids: list[int]):
    if len(sample_ids) == 1:
        context["action_sample_id"] = sample_ids[0]
    else:
        context["action_sample_id"] = None


def set_action_message(context: dict, success: bool, message: str):
    context["action_success"] = success
    context["action_message"] = message


def contour_color(color: list[int]) -> list[int]:
    r, g, b = color
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    if brightness < 90:
        return [255, 255, 255]
    else:
        return [0, 0, 0]
