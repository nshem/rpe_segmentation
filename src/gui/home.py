import os, base64, logging
from fasthtml.common import *

HOME_ID = "home"
class ImageData:
    name: str
    b64: str

    def __init__(self, b64: str, name: str):
        self.b64 = b64
        self.name = name
        
    def filename(self) -> str:
        return self.name + ".png"

def load_images() -> list[ImageData]:
    image_data: list[ImageData] = []
    try:
        for file in os.listdir(os.getenv("SAMPLES_PATH", "")):
            if not file.endswith(".png"):
                continue

            with open(os.path.join(os.getenv("SAMPLES_PATH", ""), file), "rb") as f:
                img = base64.b64encode(f.read()).decode('utf-8')
                image_name = file.split(".")[0]
                image_data.append(ImageData(b64=img,name=image_name))
    except Exception as e:
        logging.error(e)
    return image_data

def ImageActions(image_name: str):
    return [
        Button(
            "Analyse",
            hx_get=f"/analyze/{image_name}",
            hx_target="#plot",
        ),
        Button(
            "Delete",
            hx_delete=f"/{image_name}",
            hx_confirm="Are you sure you want to delete this image?",
            hx_target="#images-table",
            hx_swap="outerHTML"
        )
    ]

def ImagesTable() -> Table:
    images: list[ImageData] = load_images()

    rows = []
    for image in images:
        rows.append(
            Tr(
                Td(
                    Img(height="100%", width="70px", src=f"data:image/png;base64, {image.b64}")
                ),
                Td(image.name),
                Td(
                   *ImageActions(image_name=image.name)
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
        H2("Images"),
        Div(
            ImagesTable()
        ),
        Br(),
        H2("Upload an image"),
        ImagesForm(context.get("message", "")),
        id=HOME_ID
    )
    return Title("RPE Segmentation"), Main(home), Footer(P("© Noga Shemer 2024"))