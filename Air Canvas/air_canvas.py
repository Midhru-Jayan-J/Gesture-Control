import numpy as np
import cv2
from collections import deque

cv2.namedWindow("Color detectors")  

def setValues(x):
    print("")

cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)


while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  
        break

cv2.destroyAllWindows()
