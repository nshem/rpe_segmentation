import os
import torch
from segment_anything import modeling, sam_model_registry, SamAutomaticMaskGenerator

CHECKPOINT_PATH = os.path.join(".", "weights", "sam_vit_h_4b8939.pth")

def init_sam() -> modeling.Sam:
    DEVICE = torch.device("cpu") # or cuda/cpu if not mac
    MODEL_TYPE = "vit_h"
    print(CHECKPOINT_PATH, "; weights exist:", os.path.isfile(CHECKPOINT_PATH))
    return sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)

def init_mask_generator() -> SamAutomaticMaskGenerator:
    sam = init_sam()
    return SamAutomaticMaskGenerator(sam)
