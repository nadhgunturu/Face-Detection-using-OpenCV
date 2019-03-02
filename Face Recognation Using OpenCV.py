import cv2
import os
import numpy as np
from PIL import Image
import pickle
import sqlite3

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.save("trainer/trainerdata.yml")
cascadePath="haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascadePath)
path = "dataset"

def getProfile(id):
    conn = sqlite3.connect("DataBase.db")
    cmd = "SELECT * FROM People WHERE ID ="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
profiles = {}
while True:
    ret, im = cam.read()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Input Frame",im)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y), (x+w,y+h), (300,0,0),2)
        id, conf = recognizer.predict(gray[x:x+w,y:y+h])
        profile = getProfile(id)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = im[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,300),2)

        nose_rects = nose_cascade.detectMultiScale(roi_gray)
        for (nx,ny,nw,nh) in nose_rects:
            cv2.rectangle(roi_color,(nx,ny), (nx+nw,ny+nh), (300,0,0), 2)

        mouth_rects = mouth_cascade.detectMultiScale(roi_gray)
        for (mx,my,mw,mh) in mouth_rects:
            y = int(y - 0.15*mh)
            cv2.rectangle(roi_color, (mx,my), (mx+mw,my+mh), (0,300,0), 2)
        if(profile != None):
            cv2.cv.PutText(cv2.cv.fromarray(im),"Name:"+str(profile[1]), (x,y+h+50),font, (0,279,0))
            cv2.cv.PutText(cv2.cv.fromarray(im),"Gender:"+str(profile[2]), (x,y+h+80),font, (0,279,0))
            cv2.cv.PutText(cv2.cv.fromarray(im),"Age:"+str(profile[3]), (x,y+h+110),font, (0,279,0))
        else:
            print("Not Recognise")
            
    cv2.imshow("Face(GREEN rect),Eyes(RED rect),Nose(BLUE rect),Mouth(GREEN rect) with FaceRecognization",im)
    cv2.imwrite("Recognised Images/.jpg",im)
    cv2.waitKey(10)
    if(cv2.waitKey(1)== ord('e')):
            break                    
