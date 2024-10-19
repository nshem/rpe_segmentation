"""UI components based on fasthtml"""

import fasthtml.components as lib
import fasthtml.xtend as xlib
import fasthtml.pico as fp
from src.gui import utils

HOME_ID = "home"
SELECT_ROW_CHECKBOX_CLS = "select-row-checkbox"


def EmptyMessage() -> str:
    return lib.Small(id="message")


def Error(message: str) -> str:
    return lib.Small(message, cls="pico-color-red-500", id="message")


def Success(message: str) -> str:
    return lib.Small(message, cls="pico-color-green-500", id="message")


def Loader() -> str:
    return lib.H4(cls=f"loader mx-1", id="loader")


def RowCheckbox(sample: utils.SampleData) -> str:
    return lib.Input(
        type="checkbox",
        cls=SELECT_ROW_CHECKBOX_CLS,
        sample_id=sample.id,
    )


def ImageActions(sample: utils.SampleData):
    actions = [
        {
            "name": "Plot",
            "hx_disable": not sample.has_masks,
            "hx_post": f"/plot",
        },
        {
            "name": "Delete Masks",
            "hx_post": f"/delete_masks",
        },
        {
            "name": "Analyze",
            "hx_post": f"/analyze",
        },
        {
            "name": "Delete",
            "hx_post": f"/delete",
            "hx_confirm": "Are you sure you want to delete this sample?",
        },
    ]

    buttons = []
    for action in actions:
        buttons.append(
            lib.Button(
                action["name"],
                cls="primary pa-1",
                hx_vals=f'{{"samples": [{sample.id}]}}',
                hx_target=f"#actions-{sample.id} #message",
                hx_indicator=f"#actions-{sample.id} #loader",
                **{k: v for k, v in action.items() if k != "name"},
            )
        )

    return lib.Div(
        *buttons,
        Loader(),
        cls="d-flex ma-1 actions",
    )


def ImagesTable() -> lib.Table:
    samples: list[utils.SampleData] = utils.load_all_samples()

    rows = []
    for sample in samples:
        rows.append(
            lib.Tr(
                lib.Td(RowCheckbox(sample)),
                lib.Td(
                    lib.Img(
                        height="100%",
                        width="70px",
                        src=f"data:image/png;base64, {sample.b64}",
                    )
                ),
                lib.Td(sample.filename()),
                lib.Td("✨" if sample.has_masks else ""),
                lib.Td(
                    ImageActions(sample),
                    EmptyMessage(),
                    width="200px",
                    id=f"actions-{sample.id}",
                ),
                id=f"sample-row-{sample.id}",
                cls="sample-row",
            )
        )

    headers_text = ["", "Image", "Name", "Masks", "Actions"]
    headers = [lib.Th(header) for header in headers_text]

    return lib.Table(
        lib.Thead(lib.Tr(*headers)),
        lib.Tbody(*rows),
        id="images-table",
    )


def UploadPhotosForm(success: any, message: str) -> str:
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


def SelectionButtons() -> str:
    return [
        lib.Button(
            xlib.On(
                event="click",
                code=f"selectCheckboxesAction(true, '{SELECT_ROW_CHECKBOX_CLS}')",
            ),
            "Select all",
            cls="pico-color-purple-350 mx-1",
        ),
        lib.Button(
            xlib.On(
                event="click",
                code=f"selectCheckboxesAction(false, '{SELECT_ROW_CHECKBOX_CLS}')",
            ),
            "Deselect all",
            cls="pico-color-purple-350 mx-1",
        ),
    ]


def BatchActions() -> str:
    batch_actions = [
        {
            "name": "Plot",
            "hx_post": "/plot",
        },
        {
            "name": "Analyze",
            "hx_post": "/analyze",
        },
        {
            "name": "Delete masks",
            "hx_post": "/delete_masks",
        },
        {
            "name": "Delete sample",
            "hx_post": "/delete",
        },
    ]

    buttons = []
    for action in batch_actions:
        buttons.append(
            lib.Button(
                action["name"],
                cls="pico-color-purple-350",
                hx_post=action["hx_post"],
                hx_vals=f'js:samples: getSelectedSamples("{SELECT_ROW_CHECKBOX_CLS}")',
                hx_target="#batch-actions #message",
                hx_indicator="#batch-actions #loader",
            )
        )
    return lib.Div(
        *buttons,
        Loader(),
        EmptyMessage(),
        id="batch-actions",
        cls="d-flex",
    )


def Content(context: dict) -> str:
    return lib.Div(
        lib.H1("👁️ RPE Segmentation"),
        lib.Div(id="plot"),
        Br(),
        lib.Div(*SelectionButtons(), ImagesTable(), BatchActions()),
        Br(),
        UploadPhotosForm(
            context.get("success", None), context.get("upload_message", "")
        ),
        id=HOME_ID,
    )


def Home(context={}) -> str:
    return (
        lib.Title("RPE Segmentation"),
        lib.Main(Content(context), cls="container"),
        lib.Footer(lib.P("© Noga Shemer 2024"), cls="container"),
    )
