from selenium import webdriver
import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
import time # time 함수 사용을 위한 라이브러리 불러오기
import datetime

import app # 실시간 영상 스트리밍 관련 app.py 모듈 

import cv2
import subprocess
import os

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 부름

TRIG = 18 # TRIG 핀을 BCM 18번에 연결
ECHO = 24 # ECHO 핀을 BCM 24번에 연결
GPIO.setup(TRIG, GPIO.OUT) # 핀 모드 설정
GPIO.setup(ECHO, GPIO.IN) # 핀 모드 설정

def measure(): # 초음파 센서로 거리 측정하는 함수
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start = time.time()
    
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    
    elapsed = stop - start
    distance = (elapsed * 34300) / 2
    
    return distance

def measure_average(): # 10초동안 평균 거리 측정하는 함수
    distance1 = measure()
    time.sleep(1)
    distance2 = measure()
    time.sleep(1)
    distance3 = measure()
    time.sleep(1)
    distance4 = measure()
    time.sleep(1)
    distance5 = measure()
    time.sleep(1)
    distance6 = measure()
    time.sleep(1)
    distance7 = measure()
    time.sleep(1)
    distance8 = measure()
    time.sleep(1)
    distance9 = measure()
    time.sleep(1)
    distance10 = measure()

    distance = (distance1 + distance2 + distance3 + distance4 + distance5 + distance6 + distance7 + distance8 + distance9 + distance10) / 10
    #정밀도를 높이기 위해 1초마다 거리를 측정하여 10초동안의 평균거리 계산
    
    print(str(distance))    
    return distance

try:
    if os.path.isfile("video.mp4"):  # 기존 mp4 파일 삭제 
        os.remove("video.mp4")
    if os.path.isfile("video.avi"):  # 기존 avi 파일 삭제
        os.remove("video.avi")
        
    # 카메라 초기설정
    cap = cv2.VideoCapture(-1)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('video.avi', fourcc, 25.0, (640, 480))
    
    while True:        
        detected = 0 # 사람 감지 횟수
        nohuman = 0
        a = 0 # 초음파센서에 사람이 감지된 횟수
        flag = 0
        app.app.run(host='0.0.0.0', debug=True, threaded=True) # 실시간 영상 스트리밍
        time.sleep(1)
        
        distance = measure_average()
        time.sleep(1)
        if (distance <= 30) : # 임의 숫자 / 일정 거리 이내에 사람이 감지되면 / 테스트 후 값 수정 예정
            a = a+1 # 감지 횟수를 1씩 증가시킴 - 초음파 센서 통해 1차 확인
            while (a > 10):
                
                if GPIO.input(14) is 0: # 초인종 버튼을 눌렀을때 (기능1 중복 방지)
                    time.sleep(60) # 테스트 후 값 수정 예정
                    break
                
                while(detected < 20):
                    ret, img = cap.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
                    bodies = fullbody_cascade.detectMultiScale(gray, 1.8, 2, 0, (30, 30))
                    for (x,y,w,h) in bodies:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3, 4, 0)
                    if (ret):
                        cv2.imshow('Frame',img)
                        #print(str(len(bodies)))
                    if len(bodies) > 0:
                        detected = detected + 1
                        nohuman = 0
                        print(str(detected))
                    else:
                        nohuman = nohuman + 1
                    
                    if detected > 10: # 테스트 후 값 수정 예정
                        out.write(img)
                    
                    if nohuman == 1000: # 테스트 후 값 수정 예정
                        a = 0
                        detected = 0
                        nohuman = 0
                        flag = 1
                        break
                        
                    if cv2.waitKey(1) == ord('q'):
                        break
                if flag == 1:
                    break
        if flag == 1:
            break
                 
                cap.release()
                cv2.destroyAllWindows()
                subprocess.run('MP4Box -add video.avi video.mp4', shell=True)  # avi 파일을 mp4 파일로 변환                 
                 
                id = '~' # 카카오톡 아이디
                pw = '~' # 카카오톡 비밀번호

                KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
                ChatRoom = 'https://center-pf.kakao.com/_dLeCs/chats/4812080438129747' # 카카오톡챗봇 주소
                options = webdriver.ChromeOptions()

                # user-agent 변경
                options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")

                # 크롬 드라이버 로드
                driver = webdriver.Chrome('/lib/chromium-browser/chromedriver', options=options)
                driver.implicitly_wait(3)

                # 카카오 메인 페이지 로드
                driver.get(KaKaoURL)
                time.sleep(3)

                driver.find_element_by_id('id_email_2').send_keys(id)
                driver.find_element_by_id('id_password_3').send_keys(pw)

                driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
                time.sleep(3)

                # 채팅방 로드
                driver.get(ChatRoom)
                time.sleep(3)
                driver.find_element_by_id('chatWrite').send_keys('움직임이 감지되었습니다.') # 메세지 작성
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() # 메세지 전송 버튼
                time.sleep(5)
                driver.find_element_by_id('chatWrite').send_keys('실시간 영상 스트리밍 주소') # 메세지 작성
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() # 메세지 전송 버튼
                time.sleep(5)

                driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/button').click() # 파일 업로드 버튼
                driver.find_element_by_css_selector('#kakaoWrap > div.chat_popup > div.popup_body > div > div.write_chat2 > div.write_menu > div:nth-child(1) > div.upload_btn > input').send_keys('파일경로')
                # 짧은 영상 파일 전송 
                time.sleep(20) 

                driver.quit()
                time.sleep(60)
 
        else:
            a = 0 # 일정 거리 이내에 사람이 감지되지않음
    
finally:
    GPIO.cleanup()        
