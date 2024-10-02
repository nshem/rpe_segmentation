from fasthtml.common import *
import logging
import os
import src.gui.home as home
import base64

css = Style(href="./static/css/materialize.css", type="text/css")
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")
htmx_ws = Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
picolink = Link(rel="stylesheet", href="https://unpkg.com/pico.css/dist/pico.min.css", type="text/css")


# def upload_callback():
#     return app.redirect("/")




# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in flask.request.files:
#         return "No file part in the request"
    
#     file = flask.request.files['file']
#     if file.filename == '':
#         return "No selected file"
    
#     if file:
#         logging.warning(f"Uploading file {file.filename}")
#         file.save(os.path.join(os.getenv("SAMPLES_PATH", ""), file.filename))
#         logging.info(f"File {file.filename} uploaded successfully")
#         return app.redirect("/")

def serve_gui():

