from PIL import Image
import io
import pandas as pd
import numpy as np

from typing import Optional

from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator, colors


digit_recognizer_model = YOLO("./models/yolov8n_digit_recognizer.pt")


def get_image_from_bytes(binary_image: bytes) -> Image:
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image


def transform_predict_to_data_object(results: list, labeles_dict: dict):
    info = []
    for result in results:
        predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xywh, columns=['x', 'y', 'w','h'])
        predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf
        predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
        predict_bbox['name'] = predict_bbox["class"].replace(labeles_dict)
    return predict_bbox

def get_model_predict(model: YOLO, input_image: Image, save: bool = False, image_size: int = 1248, conf: float = 0.5, augment: bool = False) -> pd.DataFrame:

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
    
    # Transform predictions to pandas dataframe
    predictions = transform_predict_to_data_object(predictions, model.model.names)
    return predictions


def detect_sample_model(input_image: Image) -> pd.DataFrame:
    predict = get_model_predict(
        model=model_sample_model,
        input_image=input_image,
        save=False,
        image_size=640,
        augment=False,
        conf=0.5,
    )
    return predict