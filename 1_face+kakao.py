#스위치를 누르면 얼굴인식 시작 only face
#얼굴인식 후 5장의 사진 캡쳐, 저장됨

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 설정
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode

import numpy as np #얼굴 인식 후 박스로 표시 
import cv2
# Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용

try: # 키보드 인터럽트 예외처리
    count = 0
    while 1 :
       sleep(0.5)
       if GPIO.input(18) is 0:
          print('PUSH THE BUTTON')
          faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
          cap = cv2.VideoCapture(-1)
          cap.set(3,640) # set Width
          cap.set(4,480) # set Height
          while True:
             ret, img = cap.read() #img = cv2.flip(img, -1) # 상하반전
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             faces = faceCascade.detectMultiScale(
                 gray,
                 scaleFactor=1.2,
                 minNeighbors=5,
                 minSize=(20, 20)
             )
             for (x,y,w,h) in faces:
                 cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                 count += 1
                 roi_gray = gray[y:y+h, x:x+w]
                 roi_color = img[y:y+h, x:x+w]
                 cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_0" + str(count) + ".jpg", gray[y:y+h,x:x+w])
             cv2.imshow('video',img) # video라는 이름으로 출력
             k = cv2.waitKey(30) & 0xff
             if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
                break
             elif count >= 5 :
                break
          cap.release()
          cv2.destroyAllWindows()

       else:
          print('NOT PUSH THE BUTTON')
except KeyboardInterrupt:
   pass

GPIO.cleanup()


