import os
import subprocess
import torch
from segment_anything import modeling, sam_model_registry, SamAutomaticMaskGenerator

from dotenv import load_dotenv
from src.modules.sample import Sample
from src.gui import display

import sys


CHECKPOINT_PATH = os.path.join(".", "weights", "sam_vit_h_4b8939.pth")

# setup the environment
# chmod +x ./setup.sh
def setup():
    load_dotenv()

    subprocess.check_output("./setup.sh", shell=True).decode("utf-8")
    # make sure the weights are downloaded
    print(CHECKPOINT_PATH, "; weights exist:", os.path.isfile(CHECKPOINT_PATH))
    print("setup done")


def init_sam() -> modeling.Sam:
    DEVICE = torch.device("cpu") # or cuda/cpu if not mac
    MODEL_TYPE = "vit_h"
    print(CHECKPOINT_PATH, "; weights exist:", os.path.isfile(CHECKPOINT_PATH))
    return sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)

def init_mask_generator() -> SamAutomaticMaskGenerator:
    sam = init_sam()
    return SamAutomaticMaskGenerator(sam)


def main():
    mask_generator = init_mask_generator()
    samples = []
    directory = os.fsencode("./data")
    for filename in os.listdir(directory):
        filename = os.fsdecode(filename)
        print(f"processing {filename}")
        try:
            sample = Sample(filename, mask_generator)
            samples.append(sample)
        except Exception as e:
            print(f"error processing {filename}: {e}")
    print(f"proccessing done")

    display.display_multiple(samples)
    print("done")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print('running in a PyInstaller bundle')
    else:
        print('running in a normal Python process')

    main()

    # Kick off the main functionality of the application
    # data = process_data()
    # start_gui(data)

    # pyinstaller --noconfirm main.spec | ./dist/main/main