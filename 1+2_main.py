## final code ##

import RPi.GPIO as GPIO 
import time
from selenium import webdriver
import urllib

import numpy as np 
import cv2
import subprocess
import os


#GPIO pin num setting
GPIO.setmode(GPIO.BCM) 
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
GPIO.setup(17, GPIO.OUT) # set GPIO 17 as output for red led  
GPIO.setup(27, GPIO.OUT) # set GPIO 27 as output for green led  
GPIO.setup(22, GPIO.OUT) # set GPIO 22 as output for blue led

hz = 75
red = GPIO.PWM(17, hz)    # create object red for PWM on port 17  
green = GPIO.PWM(27, hz)      # create object green for PWM on port 27   
blue = GPIO.PWM(22, hz)      # create object blue for PWM on port 22 

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

# change to a larger size
def set_size(img, scale):
    return cv2.resize(img, dsize=(int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

def kakao1():
   
    #kakao setting
    
    id = ''  # personal info
    pw = '' 

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = 'https://center-pf.kakao.com/_xfxcRGs/chats/4814011526591515'
    options = webdriver.ChromeOptions()

    # Chrome driver load
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver.implicitly_wait(3)
    
    # change user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")  
          
    driver.get(KaKaoURL)
    time.sleep(1)
          
    driver.find_element_by_id('id_email_2').send_keys(id)  # write id
    driver.find_element_by_id('id_password_3').send_keys(pw)  # write password
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()  # click the input button
    sleep(1)
        
    # personal chatroom load
    driver.get(ChatRoom)
    time.sleep(1) 
                
    # write message
    driver.find_element_by_id('chatWrite').send_keys('초인종을 눌렀습니다.')  
    # When eye recognition and image storage are successful
    if count > 3 :   
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/Documents/face_detection/test_capture_03.jpg') 
          time.sleep(8)
        
          # Trained code load
          recognizer = cv2.face.LBPHFaceRecognizer_create()
          recognizer.read('/home/pi/Documents/face_detection/trainer/trainer.yml')
        
          frame = img_cap
          #cv2.imread('/home/pi/Documents/face_detection/test_capture_03.jpg')
          gray_2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
          # Get values
          id, confidence = recognizer.predict(gray_2)
          print(id)
        
          # match the name
          id = id-1
          id = names[id]
            
          # inverse 
          confidence = 100 - confidence
          if confidence < 65 :
                id = "unknown"
          
         
          # write message             
          driver.find_element_by_id('chatWrite').send_keys('외부인의 신원은 ' + str(id) + '입니다.') 
          driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() 
        
    # When eye recognition failed
    # send an alternative image that is saved immediately after press the doorbell
    else :   
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/Documents/face_detection/test_capture_who.jpg')
          driver.find_element_by_id('chatWrite').send_keys('외부인의 신원을 알 수 없습니다.') 
          driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click()
            
    time.sleep(2)        
    driver.quit()
    time.sleep(1)
    count = 0
    #exit()  # End the program
    

 def kakao2() :
    
    #kakao setting
    
    id = ''  # personal info
    pw = '' 

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = 'https://center-pf.kakao.com/_xfxcRGs/chats/4814011526591515'
    options = webdriver.ChromeOptions()

    # Chrome driver load
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver.implicitly_wait(3)
    
    # change user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")  
          
    driver.get(KaKaoURL)
    time.sleep(1)
          
    driver.find_element_by_id('id_email_2').send_keys(id)  # write id
    driver.find_element_by_id('id_password_3').send_keys(pw)  # write password
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()  # click the input button
    sleep(1)
        
    # personal chatroom load
    driver.get(ChatRoom)
    time.sleep(1) 
    
    driver.find_element_by_id('chatWrite').send_keys('움직임이 감지되었습니다.') # 메세지 작성
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() # 메세지 전송 버튼
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/button').click() # 파일 업로드 버튼
    driver.find_element_by_css_selector('#kakaoWrap > div.chat_popup > div.popup_body > div > div.write_chat2 > div.write_menu > div:nth-child(1) > div.upload_btn > input').send_keys('파일경로')
   
    # 짧은 영상 파일 전송 
    time.sleep(20) 
    driver.quit()
    time.sleep(60) # 시간 수정 예정
    
font = cv2.FONT_HERSHEY_SIMPLEX
names = ['A', 'B', 'C']  # 외부인의 신원 / id

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
    
    a = 0  # 초음파센서 감지 횟수
   
    while True:   
        flag = 0
        detected = 0 # 사람 감지 횟수
        nohuman = 0
        count = 0  # 저장할 사진의 갯수
        
        distance = measure_average()
        time.sleep(1)
        if (distance <= 50):  # 임의 숫자 / 일정 거리 이내에 사람이 감지되면 / 테스트 후 값 수정 예정
            a = a+1 # 감지 횟수를 1씩 증가시킴 - 초음파 센서 통해 1차 확인
            
        if GPIO.input(14) is 0: # 초인종 버튼을 눌렀을때 (기능1 중복 방지)
                    print('PUSH THE BUTTON')
                    # LED on
                    red.start(100)   #start red led
                    green.start(100) #start green led
                    blue.start(100)  #start blue led
         
                    now = time.time()  #time out 기능
                    # N seconds after ringing the doorbell
                    time_10 = time.time() + 10
                    time_5 = time.time() + 5
                    time_2 = time.time() + 2
        
                    # Use haarcascade_frontalface_default.xml file as Classifier
                    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
                    cap = cv2.VideoCapture(-1)
                    cap.set(3,640) # set Width
                    cap.set(4,480) # set Height
                    while True:
                        ret, img = cap.read() 
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        now = time.time()
                        # capture video and save images immediately after pressing the doorbell
                        if now < time_2 :  
                            cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_who.jpg", gray)  
                
                        eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=10, minSize=(15,15))
                        if len(eyes) :  # eye detection
                            for  x, y, w, h in eyes :
                                cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)   # show white mini box on img
                                count += 1
                                if count<6 :  # capture and save 5 images
                                    cv2.imwrite("/home/pi/Documents/face_detection/" + "test_capture_0" + str(count) + ".jpg", gray) 
                        
                        # show size-up img on monitor
                        big_size = set_size(img, 2.5)    
                        cv2.imshow("big_size", big_size)   
             
                        # When eye recognization failed
                        # send an alternative image that is saved immediately after press the doorbell
                        if count < 3 : 
                            img_who = cv2.imread('/home/pi/Documents/face_detection/test_capture_who.jpg', 1)
                            cv2.imshow('Captured Image', img_who)
                
                        # When eye recognition is successful
                        else :  
                            cv2.destroyWindow("Captured Image")  # removing the previous window
                            img_cap = cv2.imread('/home/pi/Documents/face_detection/test_capture_03.jpg', 1)
                            cv2.imshow('Recognized Image', img_cap) # show accurate image
  
                
                        k = cv2.waitKey(30) & 0xff
                        if k == 27: # press 'ESC' to quit 
                            break
                
                        # time out   
                        now = time.time()        
                        if now >= time_10 :  
                            # LED off
                            red.stop()   #stop red led
                            green.stop() #stop green led
                            blue.stop()  #stop blue led
                            GPIO.cleanup()  # clean up GPIO
                
                            if count < 3 :
                                print("no detected") 
                            break
             
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    # initialize
                    a = 0
                    detected = 0 # 사람 감지 횟수
                    nohuman = 0
                    flag = 0
                    
                    kakao1()
                    time.sleep(60) # 테스트 후 값 수정 예정
                    
                    
        while (a > 10):  # 초음파 센서로 1차 확인 이후
                while (detected < 200): # 사람의 몸 인식 / 테스트 후 값 수정 예정 / 초당 30 프레임
                    ret, img = cap.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
                    bodies = fullbody_cascade.detectMultiScale(gray, 1.8, 2, 0, (30, 30))
                    for (x,y,w,h) in bodies:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3, 4, 0)
                    if (ret):
                        cv2.imshow('Frame',img)
                        #print(str(len(bodies)))
                    if len(bodies) > 0:  # 사람의 몸 인식
                        detected = detected + 1
                       # nohuman = 0
                        print(str(detected))
                    else:
                        nohuman = nohuman + 1
                    
                    if detected > 10: # 녹화 시작 / 테스트 후 값 수정 예정
                        out.write(img)
                    
                    if nohuman == 200 : # 테스트 후 값 수정 예정
                        a = 0
                        detected = 0
                        nohuman = 0
                        flag = 1
                        break
                        
                    if cv2.waitKey(1) == ord('q'):
                        break
                if flag == 1: # 처음부터 다시 시작
                    break
       
                 
                cap.release()
                cv2.destroyAllWindows()
                subprocess.run('MP4Box -add video.avi video.mp4', shell=True)  # avi 파일을 mp4 파일로 변환                 
                
                kakao2()

    
finally:
    GPIO.cleanup()        
