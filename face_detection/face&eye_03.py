#초인종(스위치)을 누르면 LED ON, 얼굴, 눈 인식 시작
#출력 화면 크게 조정, 사이즈 조정!
#5장의 얼굴 캡쳐 & 저장 + 화면에 현재, 저장된 사진 띄우기
#time out 기능 (10sec, 15sec) & auto end!

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기
import datetime

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 설정
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
GPIO.setup(17, GPIO.OUT) #  led

import numpy as np #얼굴 인식 후 박스로 표시 
import cv2

# 크기 변경 함수
def set_size(img, scale):
    return cv2.resize(img, dsize=(int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

try: # 키보드 인터럽트 예외처리
    count = 0
    while 1 :
       sleep(0.5)
       if GPIO.input(18) is 0:
          print('PUSH THE BUTTON')
          GPIO.output(17, GPIO.HIGH) # 17번 핀을 HIGH상태로 설정합니다. LED가 켜집니다.
          now = datetime.datetime.now()  #time out
          new_now = now + datetime.timedelta(seconds =10)
          # Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용
          face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
          eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
          cap = cv2.VideoCapture(-1)
          cap.set(3,640) # set Width
          cap.set(4,480) # set Height
          while True:
             ret, img = cap.read() #img = cv2.flip(img, -1) # 상하반전
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             faces = face_cascade.detectMultiScale(gray, 1.3, 5)
             #print(len(faces)) #if 1, face detection!
             for (x,y,w,h) in faces:
                 cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                 count += 1
                 roi_gray = gray[y:y+h, x:x+w]
                 roi_color = img[y:y+h, x:x+w]
                 eyes = eye_cascade.detectMultiScale(roi_gray)
                 for (ex, ey, ew, eh) in eyes:
                     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                 if count<6 :
                    cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_0" + str(count) + ".jpg", gray) #[y-h/2:y+h+h/2,x-w/2:x+w+w/2]
             #cv2.imshow('video',img) # video라는 이름으로 출력
             big_size = set_size(img, 2.5)    #size bigger!
             cv2.imshow("big_size", big_size)      #size up 영상 출력
             if count>3 :
                 img2 = cv2.imread('/home/pi/Documents/face_detection/test_capture_03.jpg', 1)
                 cv2.imshow('Captured Image', img2)
             k = cv2.waitKey(30) & 0xff
             if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
                break
             elif count >= 5 :
                 GPIO.output(17, GPIO.LOW) # 17번 핀을 LOW 상태로 설정합니다. LED가 꺼집니다.
                 now = datetime.datetime.now()
                 if now >= new_now :
                     exit()
             now = datetime.datetime.now()          
             if now >= new_now :
                if count <1 :
                    print('no detected..')
                    GPIO.output(17, GPIO.LOW) # 17번 핀을 LOW 상태로 설정합니다. LED가 꺼집니다.
                    exit()
          cap.release()
          cv2.destroyAllWindows()

       else:
          print('NOT PUSH THE BUTTON')
except KeyboardInterrupt:
   pass

GPIO.cleanup()



