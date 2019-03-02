import cv2
import numpy as np

nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
cam=cv2.VideoCapture(0)

if nose_cascade.empty():
  raise IOError('Unable to load the nose cascade classifier xml file')

cap = cv2.VideoCapture(0)
ds_factor = 0.5

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in nose_rects:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        break

    cv2.imshow('Nose Detector', frame)

    if (cv2.waitKey(1)== ord('p')):
        break

cap.release()
cv2.destroyAllWindows()
