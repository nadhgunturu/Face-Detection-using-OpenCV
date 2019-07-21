import cv2

facedetect=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cam=cv2.VideoCapture(0)

try:
    while True:
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imshow("Input Frame",img)
        
        faces = facedetect.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(128,0,0),3)
        cv2.imshow("Output Frame",img)
        cv2.imwrite("Recognised Images/.jpg",im)
        
        if(cv2.waitKey(1)== ord('q')):
            break
except:
    KeyboardInterrupt()
    cam.release()
    cv2.destroyAllWindows()
    
