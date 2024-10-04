from src.gui.plots.sample import plot_sample
from src.modules.sample import Sample

import tempfile
import webbrowser


def display(sample: Sample):
    print("Displaying plotly")
    template = plot_sample(sample)

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        url = "file://" + f.name
        f.write(template)
    webbrowser.open(url)


def display_multiple(samples: list[Sample]):
    template = ""
    for sample in samples:
        template += plot_sample(sample)

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        url = "file://" + f.name
        f.write(template)
    webbrowser.open(url)
