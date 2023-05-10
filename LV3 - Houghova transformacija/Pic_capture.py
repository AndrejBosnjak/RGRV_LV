import cv2
import numpy as np
import json

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    c = cv2.waitKey(15)

    ret, frame = cap.read()
    cv2.imshow('Input', frame)
    image_size = frame.size

    if c == ord('c'):
        cv2.imwrite('image.jpg', frame)
        break