import numpy as np
from scipy.spatial import ConvexHull
import openpyxl
import base64
from io import BytesIO


class Coordinate:
    x: float
    y: float

    def __init__(self, l: list[float]):
        self.x = l[0]
        self.y = l[1]

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __array__(self):
        return np.array([self.x, self.y])


def calculate_angle(coords: list[list], corner_index: int) -> float:
    num_points = len(coords)

    prev = (corner_index - 1) % num_points
    next = (corner_index + 1) % num_points

    v1 = np.array(coords[prev]) - np.array(coords[corner_index])
    v2 = np.array(coords[next]) - np.array(coords[corner_index])

    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)
    angle_radians = np.arccos(
        np.clip(dot_product / (magnitude_v1 * magnitude_v2), -1.0, 1.0)
    )

    angle_degrees = np.degrees(angle_radians)
    return angle_degrees


def calculate_roundness(area: float, perimeter_length: float) -> float:
    return (4 * np.pi * area) / (perimeter_length**2)


def calculate_perimiter_length(coords: list[Coordinate]) -> float:
    return np.sum(
        [
            np.linalg.norm(np.array(coords[i]) - np.array(coords[i - 1]))
            for i in range(len(coords))
        ]
    )


def calc_centroid(coords: list[Coordinate]) -> Coordinate:
    x = [coord.x for coord in coords]
    y = [coord.y for coord in coords]
    return Coordinate([sum(x) / len(coords), sum(y) / len(coords)])


def smaller_then_third_mean(area: int, areas_mean: float) -> bool:
    return area < areas_mean / 3


def generate_xlsx_base64(data: list[list[any]]) -> str:
    wb = openpyxl.Workbook()
    ws = wb.active

    for row in data:
        ws.append(row)

    with BytesIO() as buffer:
        wb.save(buffer)
        buffer.seek(0)  # Go back to the start of the buffer

        b64_string = base64.b64encode(buffer.read()).decode("utf-8")

    return b64_string
