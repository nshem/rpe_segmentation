from src.modules.photo import Photo
from src.modules.mask import Mask, MaskReport
from src.modules.sam import generator
from src.modules import utils


class Sample:
    def __init__(self, _id: int):
        self.id = _id
        print(f"Loading sample with id {_id}")
        self.photo = Photo(_id)
        self._masks: list[Mask] = []
        self.has_masks = self.photo.has_masks()

    def generate_masks(self):
        self._masks = self.photo.generate_masks(generator)

    def report(self) -> str:
        masksReports = [MaskReport(mask).to_array() for mask in self.masks]
        masksReports.insert(0, MaskReport.to_headers_array())
        return utils.generate_xlsx_base64(masksReports)

    @classmethod
    def get_all(cls):
        return [Sample(id) for id in Photo.get_all_ids()]

    @property
    def masks(self) -> list[Mask]:
        if self.has_masks and len(self._masks) == 0:
            self._masks = self.photo.get_masks()

        return self._masks

    @property
    def filename(self) -> str:
        return self.photo.filename


def load_sample_return_image(sample: Sample) -> str:
    return sample.photo.to_png_bytes()
