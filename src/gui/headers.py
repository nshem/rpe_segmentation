from fasthtml.components import *

colors = Link(rel="stylesheet", href="./css/pico.colors.min.css", type="text/css")
utils = Link(rel="stylesheet", href="./css/utils.css", type="text/css")
htmx_ws = Script(src="./js/htmx.min.js")
row_selection = Script(src="./js/row_selection.js")

picolink = Link(rel="stylesheet", href="./css/pico.cyan.css", type="text/css")
favicon = Link(rel="icon", type="image/svg", href="./favicon.ico")

headers = (picolink, htmx_ws, row_selection, favicon, colors, utils)
