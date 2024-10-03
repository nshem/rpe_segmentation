import os
import logging
from fasthtml.common import *

from src.modules import sample
from src.gui import components, plots
from src.gui.headers import headers

debug = os.getenv("DEBUG", "True") == "True"
app, rt = fast_app(
    debug=debug,
    hdrs=headers,
    log_level="info",
    static_path="./src/gui/static",
)

context = {}


@rt("/")
def get():
    return components.Home()


@rt("/upload")
async def upload_image(request: Request):
    filenames = []
    try:
        form = await request.form()
        images = form.getlist("images")
        for image in images:
            contents = await image.read()
            with open(
                os.path.join(os.getenv("SAMPLES_PATH", ""), image.filename), "wb"
            ) as fos:
                fos.write(contents)

            filenames.append(image.filename)
        context["success"] = True
        context["upload_message"] = "Files uploaded successfully: " + ", ".join(
            filenames
        )
    except Exception as e:
        logging.error(e)
        context["success"] = False
        context["upload_message"] = "Error uploading files" + str(e)
    return components.Content(context)


@rt("/{image_name}")
def delete(image_name: str):
    try:
        os.remove(os.path.join(os.getenv("SAMPLES_PATH", ""), image_name + ".png"))
    except Exception as e:
        logging.error(e)
    return components.ImagesTable()


@rt("/analyze/{image_name}")
def get(image_name: str):
    try:
        print("Analyzing image: " + image_name)
        s = sample.Sample(image_name + ".png")
        print("Displaying image: " + image_name)
        plots.display(s)
        return components.Success(
            "Done Analyzing image: " + image_name + " - Displaying plotly in a new tab"
        )
    except Exception as e:
        logging.error(e)
    print("Done Analyzing image: " + image_name)
    return components.Error("Error analyzing image: " + image_name)
