import cv2
import numpy as np

mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
cam=cv2.VideoCapture(0)

if mouth_cascade.empty():
  raise IOError('Unable to load the mouth cascade classifier xml file')

cap = cv2.VideoCapture(0)
ds_factor = 0.5

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)
    for (x,y,w,h) in mouth_rects:
        y = int(y - 0.15*h)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,300), 3)
        break

    cv2.imshow('Mouth Detector', frame)

    if (cv2.waitKey(1)== ord('p')):
      break

cap.release()
cv2.destroyAllWindows()
