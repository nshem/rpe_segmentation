from fasthtml.common import *
import src.gui.utils as utils

HOME_ID = "home"

def ImageActions(image_name: str):
    return Group(
        Button(
            "Analyse",
            hx_get=f"/analyze/{image_name}",
            hx_target="#plot",
            cls="primary pa-1",
        ),
        Button(
            "Delete",
            cls="secondary pa-1",
            hx_delete=f"/{image_name}",
            hx_confirm="Are you sure you want to delete this image?",
            hx_target="#images-table",
            hx_swap="outerHTML",
        ),
        cls="ma-1"
    )

def ImagesTable() -> Table:
    images: list[utils.ImageData] = utils.load_images()

    rows = []
    for image in images:
        rows.append(
            Tr(
                Td(
                    Img(height="100%", width="70px", src=f"data:image/png;base64, {image.b64}")
                ),
                Td(image.name),
                Td(
                   ImageActions(image_name=image.name),
                   width="200px",
                )
            )
        )
        
    return Table(
        Thead(
            Tr(
                Th("Image"),
                Th("Name"),
                Th("Actions"),
            )
        ),
        Tbody(
            *rows
        ),
        id="images-table"
    )
    
def ImagesForm(message="") -> str:
    inp = Input(
        type="file", name="images", multiple=True, required=True, accept="image/*"
    )
    form = Form(
        Group(inp, Button("Upload")),
        hx_post="/upload",
        hx_target=f"#{HOME_ID}",
        hx_swap="outerHTML",
        enctype="multipart/form-data",
    )
    return Div(form, P(message), id="images-form")

def Home(context={}) -> str:
    home = Div(
        H1("RPE Segmentation"),
        Br(),
        Div(id="plot"),
        H2("Samples"),
        Div(
            ImagesTable()
        ),
        Br(),
        H3("Upload samples"),
        ImagesForm(context.get("message", "")),
        id=HOME_ID
    )
    return Title("RPE Segmentation"), Main(home), Footer(P("© Noga Shemer 2024"))