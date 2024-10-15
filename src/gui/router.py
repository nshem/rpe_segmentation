import os
import logging
from fasthtml.common import *

from src.modules.sample import Sample
from src.modules.photo import Photo
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
            Photo.create_new(_filename=image.filename, _bytes=contents)
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


@rt("/{id}")
def delete(id: int):
    try:
        Photo(id).delete()
    except Exception as e:
        logging.error(e)
    return components.ImagesTable()


@rt("/analyze/{id}")
def get(id: int):
    try:
        s = Sample(id)
        if len(s.masks) == 0:
            print("Generating masks")
            s.generate_masks()

        plots.display(s)
        return components.Success(
            f"Done Analyzing image: {id} - Displaying plotly in a new tab"
        )
    except Exception as e:
        logging.error(e)
    print(f"Done Analyzing image: {id}")
    return components.Error(f"Error analyzing image: {id}")
