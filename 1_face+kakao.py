#초인종(스위치)을 누르면 LED ON, 사람의 눈 인식 시작
#눈만 인식함으로써 마스크를 착용했을 때에도 인식
#초인종 누른 직후 임의 저장된 이미지 + 현재 문 앞 상황 동시 송출
#if 얼굴인식 성공, 5장의 얼굴 캡쳐 및 저장->이전 창 닫기 + 인식된 (정확한) 얼굴로 대신 송출
#화면 사이즈 변경->전체 화면으로 띄우기
#time out 기능 (10sec) & auto end
#카카오 챗봇 기능 추가 & 인터폰 기능 종료 후 카카오톡 접속 & '초인종 눌렀습니다' 출력


import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기
import datetime
from selenium import webdriver
import urllib

#GPIO 핀 번호 setting
GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 설정
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
GPIO.setup(17, GPIO.OUT) #  led

import numpy as np #얼굴 인식 후 박스로 표시 
import cv2

# 크기 변경 함수
def set_size(img, scale):
    return cv2.resize(img, dsize=(int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

def kakao():
    
    #kakao setting
    id = ''  #개인 아이디
    pw = ''  #개인 비밀번호

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = 'https://center-pf.kakao.com/_xfxcRGs/chats/4814011526591515'
    options = webdriver.ChromeOptions()

    #크롬 드라이버 로드
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver.implicitly_wait(3)
    
    #user-agent 변경
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")  
          
    driver.get(KaKaoURL)
    sleep(1)
          
    driver.find_element_by_id('id_email_2').send_keys(id)  #아이디 작성
    driver.find_element_by_id('id_password_3').send_keys(pw)  #비밀번호 작성
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()  #입력버튼 클릭
    sleep(1)
        
    #채팅방 로드
    driver.get(ChatRoom)
    sleep(1)
        
    #글 작성
    driver.find_element_by_id('chatWrite').send_keys('초인종을 눌렀습니다.')  #메시지 작성
    if count > 3 :   #얼굴인식 및 이미지 저장이 잘 되었을 경우
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/Documents/face_detection/test_capture_03.jpg') 
    else :    #얼굴인식이 안되었을 경우, 초인종 누른 직후 임의 캡쳐한 이미지를 대신 전달
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/Documents/face_detection/test_capture_who.jpg')
          
    driver.quit()
    sleep(1)
    exit()  #프로그램 종료
   

try: # 키보드 인터럽트 예외처리
    count = 0  #initialize
    while 1 :
       sleep(0.5)
       if GPIO.input(18) is 0:
          print('PUSH THE BUTTON')
        
          GPIO.output(17, GPIO.HIGH) # 17번 핀을 HIGH상태로 설정합니다. LED가 켜집니다.
          now = datetime.datetime.now()  #time out 기능
          time_10 = now + datetime.timedelta(seconds =10)  #초인종을 누른 후 10초 지남
          time_5 = now + datetime.timedelta(seconds =5)  #초인종을 누른 후 5초 지남
          time_2 = now + datetime.timedelta(seconds =2)   #초인종을 누른 후 2초 지남
        
          #haarcascade_frontalface_default.xml 파일을 Classifier로 사용
          eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
          cap = cv2.VideoCapture(-1)
          cap.set(3,640) # set Width
          cap.set(4,480) # set Height
          while True:
             ret, img = cap.read() 
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             now = datetime.datetime.now() 
             if now < time_2 :  #초인종을 누른 직후 이미지 임의 캡쳐 및 저장
                cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_who.jpg", gray)  
                
             eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.1, minNeighbors=10, minSize=(15,15))
             if len(eyes) :  #사람의 눈 인식
                 for  x, y, w, h in eyes :
                     cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)   #white mini box
                     count += 1
                     if count<6 :  #5장의 이미지 캡쳐 및 저장
                         cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_0" + str(count) + ".jpg", gray) 
                        
             #size up 영상 출력
             big_size = set_size(img, 2.5)    
             cv2.imshow("big_size", big_size)   
             
             if count < 3 :  #얼굴인식이 안되었을 때, 초인종 누른 직후 임의 저장된 이미지 대신 송출
                img_who = cv2.imread('/home/pi/Documents/face_detection/test_capture_who.jpg', 1)
                cv2.imshow('Captured Image', img_who)
             
             else :  #얼굴인식이 성공적으로 진행
                cv2.destroyWindow("Captured Image")  #이전의 창 제거 후 정확한 사진 송출
                img_cap = cv2.imread('/home/pi/Documents/face_detection/test_capture_03.jpg', 1)
                cv2.imshow('Recognized Image', img_cap)
  
                
             k = cv2.waitKey(30) & 0xff
             if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
                break
                
             #time out   
             now = datetime.datetime.now()          
             if now >= time_10 :  
                GPIO.output(17, GPIO.LOW) # 17번 핀을 LOW 상태로 설정합니다. LED가 꺼집니다.
                if count < 3 :
                    print("no detected") 
                break
             
          cap.release()
          cv2.destroyAllWindows()
          kakao()
            
       else:
          print('NOT PUSH THE BUTTON')
            
except KeyboardInterrupt:
   pass

GPIO.cleanup()


