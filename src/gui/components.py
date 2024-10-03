"""UI components based on fasthtml"""

import fasthtml.components as lib
import fasthtml.pico as fp
from src.gui import utils

HOME_ID = "home"


def EmptyMessage() -> str:
    return lib.Small(id="message")


def Error(message: str) -> str:
    return lib.Small(message, cls="pico-color-red-500", id="message")


def Success(message: str) -> str:
    return lib.Small(message, cls="pico-color-green-500", id="message")


def Loader() -> str:
    return lib.H4(cls=f"loader mx-1", id="loader")


def ImageActions(image_name: str):
    return lib.Div(
        Loader(),
        lib.Button(
            "Analyze",
            hx_get=f"/analyze/{image_name}",
            hx_target=f"#actions-{image_name} #message",
            hx_indicator=f"#actions-{image_name} #loader",
            cls="primary pa-1",
        ),
        lib.Button(
            "Delete",
            cls="secondary pa-1",
            hx_delete=f"/{image_name}",
            hx_confirm="Are you sure you want to delete this image?",
            hx_target="#images-table",
            hx_swap="outerHTML",
        ),
        cls="d-flex ma-1",
    )


def ImagesTable() -> lib.Table:
    images: list[utils.ImageData] = utils.load_images()

    rows = []
    for image in images:
        rows.append(
            lib.Tr(
                lib.Td(
                    lib.Img(
                        height="100%",
                        width="70px",
                        src=f"data:image/png;base64, {image.b64}",
                    )
                ),
                lib.Td(image.name),
                lib.Td(
                    ImageActions(image_name=image.name),
                    EmptyMessage(),
                    width="200px",
                    id=f"actions-{image.name}",
                ),
            )
        )

    return lib.Table(
        lib.Thead(
            lib.Tr(
                lib.Th("Image"),
                lib.Th("Name"),
                lib.Th("Actions"),
            )
        ),
        lib.Tbody(*rows),
        id="images-table",
    )


def ImagesForm(success: any, message: str) -> str:
    inp = lib.Input(
        type="file", name="images", multiple=True, required=True, accept="image/*"
    )
    message_comp = EmptyMessage()
    if success is not None:
        message_comp = Success(message) if success else Error(message)

    form = lib.Form(
        fp.Div(inp, lib.Button("Upload"), cls="d-flex"),
        message_comp,
        hx_post="/upload",
        hx_target=f"#{HOME_ID}",
        hx_swap="innerHTML",
        enctype="multipart/form-data",
    )

    return lib.Div(form, id="images-form")


def Br() -> str:
    return lib.H4(
        "...........................................................................",
        cls="text-truncate text-center",
    )


def Content(context: dict) -> str:
    return lib.Div(
        lib.H1("RPE Segmentation"),
        lib.Div(id="plot"),
        Br(),
        lib.Div(ImagesTable()),
        Br(),
        ImagesForm(context.get("success", None), context.get("upload_message", "")),
        id=HOME_ID,
    )


def Home(context={}) -> str:
    return (
        lib.Title("RPE Segmentation"),
        lib.Main(Content(context), cls="container"),
        lib.Footer(lib.P("© Noga Shemer 2024"), cls="container"),
    )
