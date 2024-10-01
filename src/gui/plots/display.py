from src.gui.plots.sample import plot_sample
from src.modules.sample import Sample

import base64
import tempfile
import webbrowser
from src.gui.home import render_home

def display(sample: Sample):
    template = render_home(image_data=sample.photo.to_png_bytes())

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(template)
    webbrowser.open(url)

def display_plotly(sample: Sample):
    template = plot_sample(sample)

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(template)
    webbrowser.open(url)

def display_multiple(samples: list[Sample]):
    template = ""
    for sample in samples:
        template += plot_sample(sample)

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(template)
    webbrowser.open(url)