import os
import logging

import src.gui.router as router
import src.modules.sample as sample
import src.modules.sam as sam

generator = sam.init_mask_generator()

if __name__ == '__main__':
    os.environ["SAMPLES_PATH"] = "input"
    router.app_run()