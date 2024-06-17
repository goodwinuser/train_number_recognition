from PIL import Image
import io
import pandas as pd
import numpy as np

from typing import Optional

from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator, colors


number_detecting_model = YOLO("./models/yolov8n_number_detecting.pt")


def transform_predict_to_data_object(results: list, labeles_dict: dict):
    info = []
    for result in results:
        predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xywh, columns=['x', 'y', 'w','h'])
        predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf
        predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
        predict_bbox['name'] = predict_bbox["class"].replace(labeles_dict)
    return predict_bbox

def get_model_predict(model: YOLO, input_image: Image, save: bool = False, image_size: int = 640, conf: float = 0.5, augment: bool = False):
    predictions = model.predict(
                        imgsz=image_size, 
                        source=input_image, 
                        conf=conf,
                        save=save, 
                        augment=augment,
                        flipud= 0.0,
                        fliplr= 0.0,
                        mosaic = 0.0,
                        )
    

    predictions = transform_predict_to_data_object(predictions, model.model.names)
    return predictions

 
def detect_digits(input_image: Image):
    """
    Распознание цифры в номере
    Args:
        input_image (Image): изображение

    Returns:
        данные об обнаруженной цифре
    """
    predict = get_model_predict(
        model=digit_recognizer_model,
        input_image=input_image,
        save=False,
        image_size=640,
        augment=False,
        conf=0.5,
    )
    return predict


def recognize__digits(input_image: Image):
    digits_data = detect_digits(input_image)
    
    return digits_data