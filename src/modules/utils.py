import numpy as np

def calculate_angle(coords: list[list], corner_index: int) -> float:
    num_points = len(coords)
    
    prev = (corner_index - 1) % num_points
    next = (corner_index + 1) % num_points
    
    v1 = np.array(coords[prev]) - np.array(coords[corner_index])
    v2 = np.array(coords[next]) - np.array(coords[corner_index])

    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)
    angle_radians = np.arccos(np.clip(dot_product / (magnitude_v1 * magnitude_v2), -1.0, 1.0))

    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

def smaller_then_third_mean(area: int, areas_mean: float) -> bool:
    return area < areas_mean / 3
