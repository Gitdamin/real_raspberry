#초인종(스위치)을 누르면 LED ON, 얼굴, 눈 인식 시작
#얼굴 인식 박스 표시 위에 'outsider detected' 출력
#5장의 얼굴 캡쳐 & 저장 + 화면에 현재, 저장된 사진 띄우기
#화면 사이즈 변경-전체 화면으로 띄우기
#time out 기능 (10sec, 15sec) & auto end
#카카오 챗봇 기능 추가 & 인터폰 기능 종료 후 카카오톡 접속 & '초인종 눌렀습니다' 출력

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기
import datetime

#kakao_use
from selenium import webdriver
from PIL import Image
import configparser
import urllib

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 설정
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
GPIO.setup(17, GPIO.OUT) #  led

import numpy as np #얼굴 인식 후 박스로 표시 
import cv2

font = cv2.FONT_ITALIC

# 크기 변경 함수
def set_size(img, scale):
    return cv2.resize(img, dsize=(int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

#kakao_setting
id = ''
pw = ''

KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
ChatRoom = 'https://center-pf.kakao.com/_xfxcRGs/chats/4814011526591515'
options = webdriver.ChromeOptions()

try: # 키보드 인터럽트 예외처리
    count = 0
    while 1 :
       sleep(0.5)
       if GPIO.input(18) is 0:
          print('PUSH THE BUTTON')
        
          GPIO.output(17, GPIO.HIGH) # 17번 핀을 HIGH상태로 설정합니다. LED가 켜집니다.
          now = datetime.datetime.now()  #time out
          time_10 = now + datetime.timedelta(seconds =10)
          time_15 = now + datetime.timedelta(seconds =15)
        
          #haarcascade_frontalface_default.xml 파일을 Classifier로 사용
          face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
          eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
          cap = cv2.VideoCapture(-1)
          cap.set(3,640) # set Width
          cap.set(4,480) # set Height
          while True:
             ret, img = cap.read() #img = cv2.flip(img, -1) # 상하반전
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
             for (x,y,w,h) in faces:
                 cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                 count += 1
                 roi_gray = gray[y:y+h, x:x+w]
                 roi_color = img[y:y+h, x:x+w]
                 eyes = eye_cascade.detectMultiScale(roi_gray)
                 for (ex, ey, ew, eh) in eyes:
                     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                     cv2.putText(img, "Outsider detected", (x-5, y-5), font, 1, (0,255,0),2)  #얼굴찾았다는 메시지, green color
                 if count<6 :
                    cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_0" + str(count) + ".jpg", gray) 
                 
             #cv2.imshow('video',img) # video라는 이름으로 출력
             big_size = set_size(img, 2.5)    #size bigger
             cv2.imshow("big_size", big_size)     #size up 영상 출력
             if count>3 :
                 img2 = cv2.imread('/home/pi/Documents/face_detection/test_capture_03.jpg', 1)
                 cv2.imshow('Captured Image', img2)
             k = cv2.waitKey(30) & 0xff
             if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
                break
             elif count >= 5 :
                 GPIO.output(17, GPIO.LOW) # 17번 핀을 LOW 상태로 설정합니다. LED가 꺼집니다.
                 now = datetime.datetime.now()
                 if now >= time_10 :
                     break
             now = datetime.datetime.now()          
             if now >= time_15 :
                if count <1 :
                    print('no detected..')
                    GPIO.output(17, GPIO.LOW) # 17번 핀을 LOW 상태로 설정합니다. LED가 꺼집니다.
                    break
             
          cap.release()
          cv2.destroyAllWindows()
            
          #kakao
          #크롬 드라이버 로드
          driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
          driver.implicitly_wait(3)
          #user-agent 변경
          options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")  
          
          driver.get(KaKaoURL)
          sleep(1)
          
          driver.find_element_by_id('id_email_2').send_keys(id)
          driver.find_element_by_id('id_password_3').send_keys(pw)
          driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
          sleep(1)
        
          #채팅방 로드
          driver.get(ChatRoom)
          sleep(1)
        
          #글 작성
          driver.find_element_by_id('chatWrite').send_keys('초인종을 눌렀습니다.')  #메시지 작성
          driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click()  #전송버튼
          #//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button
          sleep(3)
          driver.quit()
          sleep(1)
          exit()
   

       else:
          print('NOT PUSH THE BUTTON')
except KeyboardInterrupt:
   pass

GPIO.cleanup()


