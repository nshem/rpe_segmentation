from fasthtml.components import *

colors = Link(rel="stylesheet", href="./css/pico.colors.min.css", type="text/css")
css_utils = Link(rel="stylesheet", href="./css/utils.css", type="text/css")
htmx_ws = Script(src="./js/htmx.min.js")
js_utils = Script(src="./js/utils.js")
picolink = Link(rel="stylesheet", href="./css/pico.cyan.min.css", type="text/css")
favicon = Link(rel="icon", type="image/svg", href="./favicon.ico")

headers = (picolink, htmx_ws, js_utils, favicon, colors, css_utils)
