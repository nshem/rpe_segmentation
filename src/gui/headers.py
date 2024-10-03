from fasthtml.components import *

colors = Link(rel="stylesheet", href="./css/pico.colors.min.css", type="text/css")
utils = Link(rel="stylesheet", href="./css/utils.css", type="text/css")
gridlink = Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css",
)
htmx_ws = Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
picolink = Link(rel="stylesheet", href="./css/pico.cyan.css", type="text/css")
favicon = Link(rel="icon", type="image/x-icon", href="./favicon.ico")

headers = (picolink, gridlink, htmx_ws, favicon, colors, utils)
