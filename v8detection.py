from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
from ultralytics.yolo.utils.ops import non_max_suppression
import cv2
import torch

def find_cordinates(img):

    model = YOLO("yolov8m.pt")
    results = model.predict(source=img, classes= 59)
    for result in results:
        boxes = result.boxes
        cordnates = boxes.xywh
        lis = cordnates.tolist()
        return lis