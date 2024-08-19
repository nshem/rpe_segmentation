import cv2, os
import numpy as np
import os
from segment_anything import SamAutomaticMaskGenerator
import cv2
from typing import Dict
import numpy as np
from src.modules.photo import Photo

class Sample:
    def __init__(self, _file_name: str, mask_generator: SamAutomaticMaskGenerator):
        self.photo = Photo(_file_name)
        self.masks = self.photo.generate_masks(mask_generator)

