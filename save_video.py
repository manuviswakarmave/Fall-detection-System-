import cv2
from utils.datasets import letterbox

def save_vid(frame,width,height):
    size = (width,height)
    out = cv2.VideoWriter('fall_detected.mp4', 
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         30, size)
    
