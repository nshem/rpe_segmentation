import os
import logging

import src.modules.sample as sample
import src.gui.plots.display as display
import src.modules.sam as sam

from fasthtml.common import *
import src.gui.components as components

css = Style(href="./static/css/materialize.css", type="text/css")
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")
htmx_ws = Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
picolink = Link(rel="stylesheet", href="https://unpkg.com/pico.css/dist/pico.min.css", type="text/css")

logging.info("Serving GUI")
debug = os.getenv("DEBUG", "True") == "True"
app,rt = fast_app(debug=debug, hdrs=(picolink, gridlink, css, htmx_ws), log_level="info", static_path="./gui")

context = {}
generator = sam.init_mask_generator()

@rt('/')
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
            with open(os.path.join(os.getenv("SAMPLES_PATH", ""), image.filename), "wb") as fos:
                fos.write(contents)
            
            filenames.append(image.filename)
        context["message"] = "Files uploaded successfully: " + ", ".join(filenames)
    except Exception as e:
        logging.error(e)
        context["message"] = "Error uploading files" + str(e)
    return components.Home(context)

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
        s = sample.Sample(image_name + ".png", generator)
        print("Displaying image: " + image_name)
        display.display_plotly(s)
        return P("Done Analyzing image: " + image_name + " - Displaying plotly in a new tab")
    except Exception as e:
        logging.error(e)
    print("Done Analyzing image: " + image_name)
    return P("Error analyzing image: " + image_name)
