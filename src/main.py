import os
from src.gui.router import *
from fasthtml.common import *

if __name__ == '__main__':
    os.environ["SAMPLES_PATH"] = "./input"
    serve(appname="src.gui.router", app="app")
