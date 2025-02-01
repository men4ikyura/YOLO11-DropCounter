import json
import numpy as np

from PIL import Image
from shapely.geometry import Polygon
from ultralytics import YOLO


def processing_image(path_image, conf, iou, retina_masks, imgsz, multiplier_from_pixels_to_microns):

    with open("./settings.json") as file:
        data = json.load(file)
        model_path = data.get("model_path", None)
        if model_path is None:
            raise Exception("Выберите путь до модели в настройках")

    model = YOLO(model_path)

    image = Image.open(path_image)

    result = model(image, imgsz=imgsz, conf=conf, iou=iou,
                   retina_masks=retina_masks, max_det=2500)

    if result[0].masks == None:
        return (0, [])

    masks = result[0].masks.xy

    result_list = make_result_list(masks, multiplier_from_pixels_to_microns)

    return (len(result_list), result_list)


def count_all_parameters_of_object_on_image(mask, multiplier_from_pixels_to_microns):
    if len(mask.astype(set)) > 3:
        new_mask = np.vstack([mask, mask[0]])
        polygon = Polygon(new_mask)
        center = polygon.centroid
        diameter = find_diameter_in_pixels(
            new_mask, center) / multiplier_from_pixels_to_microns
        return (new_mask, diameter, (center.x, center.y))
    return None


def make_result_list(masks, multiplier_from_pixels_to_microns):
    res_list = []
    for mask in masks:
        res_tuple = count_all_parameters_of_object_on_image(
            mask, multiplier_from_pixels_to_microns)
        if res_tuple != None:
            res_list.append(res_tuple)
    return res_list


def find_diameter_in_pixels(mask, center_point):
    distances = np.sqrt((mask[:, 0] - center_point.x) **
                        2 + (mask[:, 1] - center_point.y)**2)
    return float(distances.mean() * 2)
