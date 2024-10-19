import os
import logging
import json
from fasthtml.common import *

from src.modules.sample import Sample
from src.modules.photo import Photo
from src.gui import components, plots, utils
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


@rt("/delete")
async def post(request: Request):
    try:
        sample_ids = await utils.extract_sample_ids_from_request(request)
        utils.set_action_target(context, sample_ids)

        for sample_id in sample_ids:
            Photo(sample_id).delete()

        utils.set_action_message(context, True, f"Deleted images: {sample_ids}")
    except Exception as e:
        logging.error(e)
        utils.set_action_message(
            context, False, f"Error deleting {sample_ids}: " + str(e)
        )
    return components.Content(context)


@rt("/delete_masks")
async def post(request: Request):
    try:
        sample_ids = await utils.extract_sample_ids_from_request(request)
        utils.set_action_target(context, sample_ids)

        for sample_id in sample_ids:
            Sample(sample_id).photo.delete_masks()

        utils.set_action_message(
            context, True, f"Deleted masks for samples: {sample_ids}"
        )
    except Exception as e:
        logging.error(e)
        utils.set_action_message(
            context, False, f"Error deleting masks for {sample_ids}: " + str(e)
        )
    return components.Content(context)


@rt("/plot")
async def post(request: Request):
    try:
        sample_ids = await utils.extract_sample_ids_from_request(request)
        utils.set_action_target(context, sample_ids)

        for sample_id in sample_ids:
            id = int(sample_id)
            sample = Sample(id)
            if len(sample.masks) == 0:
                raise Exception("No masks found: " + sample.filename)
            plots.display(sample)

        utils.set_action_message(
            context, True, f"Plotted selected images: {sample_ids}"
        )
    except Exception as e:
        logging.error(e)
        utils.set_action_message(
            context, False, f"Error plotting selected images {sample_ids}: " + str(e)
        )
    return components.Content(context)


@rt("/analyze")
async def post(request: Request):
    try:
        sample_ids = await utils.extract_sample_ids_from_request(request)
        utils.set_action_target(context, sample_ids)

        for sample_id in sample_ids:
            Sample(sample_id).generate_masks()

        utils.set_action_message(
            context, True, f"Done Analyzing selected images: {sample_ids}"
        )
    except Exception as e:
        logging.error(e)
        utils.set_action_message(
            context, False, f"Error analyzing selected images {sample_ids}: " + str(e)
        )
    return components.Content(context)
