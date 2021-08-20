## Data set code ##
# capture and save faces per id 

import cv2
import os
from time import sleep
import datetime

cam = cv2.VideoCapture(-1)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

# using haar_eyedetect
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# For each person, enter one numeric face id
face_id = input('\n write id and push the enter button => ')
print("\n [INFO] Initializing face capture...")

# Initialize individual sampling face count
count = 0

while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.1, minNeighbors= 10, minSize=(15,15))
    
    for  x, y, w, h in eyes :
        # show white box on img
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4) 
        count += 1
        # Save the captured image into the datasets folder
        if count < 30 :
           cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray)
        
       
    cv2.imshow('image', img)
    
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
  
print("\n [INFO] End the program.")
cam.release()
cv2.destroyAllWindows()
