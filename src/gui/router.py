import flask
import logging
import os
import src.gui.home as home
import base64

app = flask.Flask(__name__)

def upload_callback():
    return app.redirect("/")

@app.route('/')
def index():
    image_data = []
    try:
        for file in os.listdir(os.getenv("SAMPLES_PATH", "")):
            if not file.endswith(".png"):
                continue

            with open(os.path.join(os.getenv("SAMPLES_PATH", ""), file), "rb") as f:
                img = base64.b64encode(f.read()).decode('utf-8')
                image_data.append({"b64": img, "name": file})
    except Exception as e:
        logging.error(e)
    return home.render(upload_callback=upload_callback, image_data=image_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in flask.request.files:
        return "No file part in the request"
    
    file = flask.request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        logging.warning(f"Uploading file {file.filename}")
        file.save(os.path.join(os.getenv("SAMPLES_PATH", ""), file.filename))
        logging.info(f"File {file.filename} uploaded successfully")
        return app.redirect("/")

def app_run():
    debug = os.getenv("DEBUG", "True") == "True"
    app.run(debug=debug, port=5005)