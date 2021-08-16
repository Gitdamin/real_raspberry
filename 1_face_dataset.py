##사람의 눈 인식 후 이미지 저장 코드##
#새롭게 학습하고 싶은 인물을 촬영 

import cv2
import os
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기
import datetime

cam = cv2.VideoCapture(-1)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# For each person, enter one numeric face id
face_id = input('\n write your id and push the enter button => ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

# Initialize
count = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.1, minNeighbors= 10, minSize=(15,15))
    
    for  x, y, w, h in eyes :
        #얼굴 인식
        #now = datetime.datetime.now()  #time out
        #time_2 = now + datetime.timedelta(seconds =2)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4) #white mini box
        count += 1
        # Save the captured image into the datasets folder
        if count < 10 :
           cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray)
        
       
    cv2.imshow('image', img)
    
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    #elif count >= 30: # Take 30 face sample and stop video
         #break
# Do a bit of cleanup

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
