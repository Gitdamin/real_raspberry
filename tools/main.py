## final code ##

import RPi.GPIO as GPIO 
import time
from selenium import webdriver
import urllib

import numpy as np 
import cv2
import subprocess
import os


def measure(): # measure distance using Ultra.
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

def measure_average():  # mean distance / no time.sleep() 
  while 1 :  
    n = 0
    distance = 0
    now = time.time()
    time_10 = now + 10
    
    while 1 :
        n += 1
        distance += measure()
        
        now = time.time()
        if now > time_10 :
            break
        
        if GPIO.input(14) is 0:
            break
    
    distance = distance / n
    print('평균거리')  # checking
    print(str(distance))    
    return distance

font = cv2.FONT_HERSHEY_SIMPLEX
names = []  # fill the blank

# change to a larger size
def set_size(img, scale):
    return cv2.resize(img, dsize=(int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

def kakao1():
   
    #kakao setting
    
    id = ''  # personal info
    pw = '' 

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = '~'
    options = webdriver.ChromeOptions()

    # Chrome driver load
    driver = webdriver.Chrome('./src/chromedriver', options=options)
    driver.implicitly_wait(3)
    
    # change user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")  
          
    driver.get(KaKaoURL)
    time.sleep(1)
          
    driver.find_element_by_id('id_email_2').send_keys(id)  # write id
    driver.find_element_by_id('id_password_3').send_keys(pw)  # write password
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()  # click the input button
    time.sleep(1)
        
    # personal chatroom load
    driver.get(ChatRoom)
    time.sleep(1) 
                
    # write message
    driver.find_element_by_id('chatWrite').send_keys('초인종을 눌렀습니다.')  
    # When eye recognition and image storage are successful
    if count > 3 :   
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('./testset/store_3.jpg') 
          time.sleep(8)
        
          # Trained code load
          recognizer = cv2.face.LBPHFaceRecognizer_create()
          recognizer.read('./trainer/trainer.yml')
        
          frame = img_cap
          #cv2.imread('./testset/store_3.jpg')
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
        
          if id == '성범죄자' :
            driver.find_element_by_id('chatWrite').send_keys('[위험] 해당 외부인이 성범죄자일 확률이 ' + str(confidence) + '% 입니다.')  
            driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() 
        
    # When eye recognition failed
    # send an alternative image that is saved immediately after press the doorbell
    else :   
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('./testset/capture.jpg')
          driver.find_element_by_id('chatWrite').send_keys('외부인의 신원을 알 수 없습니다.') 
          driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click()
            
    time.sleep(2)        
    driver.quit()
    time.sleep(1)
    
    #exit()  # End the program
    

def kakao2() :
    
    #kakao setting
    
    id = ''  # personal info
    pw = '' 

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = '~'
    options = webdriver.ChromeOptions()

    # Chrome driver load
    driver = webdriver.Chrome('./src/chromedriver', options=options)
    driver.implicitly_wait(3)
    
    # change user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")  
          
    driver.get(KaKaoURL)
    time.sleep(1)
          
    driver.find_element_by_id('id_email_2').send_keys(id)  # write id
    driver.find_element_by_id('id_password_3').send_keys(pw)  # write password
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()  # click the input button
    time.sleep(1)
        
    # personal chatroom load
    driver.get(ChatRoom)
    time.sleep(1) 
    
    # write message
    driver.find_element_by_id('chatWrite').send_keys('움직임이 감지되었습니다.') 
    driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() 
    driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('./video/video.mp4')
      
    time.sleep(2) 
    driver.quit()
    time.sleep(1) 
  

# Setting the distance between the doorbell and the opposite wall
num = 0

try:
    if os.path.isfile("video.mp4"):  # Delete the existing .mp4 file
        os.remove("video.mp4")
    if os.path.isfile("video.avi"):  # Delete the existing .avi file
        os.remove("video.avi")
        
    # Initial camera setting
    cap = cv2.VideoCapture(-1)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + './src/haarcascade_fullbody.xml')
    upperbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + './src/haarcascade_upperbody.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + './src/haarcascade_eye.xml')
    
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('video.avi', fourcc, 25.0, (640, 480))
    
    a = 0  # The number of ultrasonic sensors detected
   
    while True:   
        flag = 0
        detected = 0 # The number of people detected
        nohuman = 0
        count = 0  # The number of photos to save
        
        #GPIO pin num setting / prevention of time out 
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
        GPIO.setup(17, GPIO.OUT) # set GPIO 17 as output for red led  
        GPIO.setup(27, GPIO.OUT) # set GPIO 27 as output for green led  
        GPIO.setup(22, GPIO.OUT) # set GPIO 22 as output for blue led

        TRIG = 18 
        ECHO = 24 
        GPIO.setup(TRIG, GPIO.OUT) 
        GPIO.setup(ECHO, GPIO.IN)
        
        if num < 1 :  # initialize distance
            num = measure_average()
            
        distance = measure_average()
        
        if (distance <= num - 25):  # Error -25cm
            
            a = a+1  # First confirmation through ultrasonic sensor
            print(a)  # checking 
            
        if GPIO.input(14) is 0:  # if push the button, (Prevent duplication of functions)
                    
                    print('PUSH THE BUTTON') # checking
                    
                    # LED on
                    hz = 75
                    red = GPIO.PWM(17, hz)    # create object red for PWM on port 17  
                    green = GPIO.PWM(27, hz)      # create object green for PWM on port 27   
                    blue = GPIO.PWM(22, hz)      # create object blue for PWM on port 22 
                    
                    red.start(100)   #start red led
                    green.start(100) #start green led
                    blue.start(100)  #start blue led
         
                    now = time.time()  # time out function
                    # N seconds after ringing the doorbell
                    time_10 = time.time() + 10
                    time_5 = time.time() + 5
                    time_2 = time.time() + 2
        
                    # Use haarcascade_frontalface_default.xml file as Classifier
                    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + './src/haarcascade_eye.xml')
                   
                    while True:
                        ret, img = cap.read() 
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        now = time.time()
                        # capture video and save images immediately after pressing the doorbell
                        if now < time_2 :  
                            cv2.imwrite("./testset/capture.jpg", gray)  
                
                        eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=10, minSize=(15,15))
                        if len(eyes) :  # eye detection
                            for  x, y, w, h in eyes :
                                cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)   # show white mini box on img
                                count += 1
                                if count<6 :  # capture and save 5 images
                                    cv2.imwrite("./testset/" + "store_" + str(count) + ".jpg", gray) 
                        
                        # show size-up img on monitor
                        big_size = set_size(img, 2.5)    
                        cv2.imshow("big_size", big_size)   
             
                        # When eye recognization failed
                        # send an alternative image that is saved immediately after press the doorbell
                        if count < 3 : 
                            img_who = cv2.imread('./testset/capture.jpg', 1)
                            cv2.imshow('Captured Image', img_who)
                
                        # When eye recognition is successful
                        else :  
                            cv2.destroyWindow("Captured Image")  # removing the previous window
                            img_cap = cv2.imread('./testset/store_3.jpg', 1)
                            cv2.imshow('Recognized Image', img_cap) # show accurate image
  
                
                        k = cv2.waitKey(30) & 0xff
                        if k == 27: # press 'ESC' to quit
                            GPIO.cleanup()   
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
             
                    #cap.release()
                    cv2.destroyAllWindows()
                    
                    # initialize
                    a = 0
                    detected = 0 
                    nohuman = 0
                    flag = 0
                    
                    kakao1()
                    time.sleep(10) 
                    
                    
        while (a > 6): 
                while (detected < 50): # 2nd confirmation through human body recognition / about 2~4 sec 
                    ret, img = cap.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
                    bodies = fullbody_cascade.detectMultiScale(gray, 1.8, 2, 0, (30, 30))
                    upper_bodies = upperbody_cascade.detectMultiScale(gray, 1.5, 2, 0, (30, 30))
                    eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=10, minSize=(15,15)) # increase the accuracy
                   
                    for (x,y,w,h) in bodies:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),3, 4, 0)
                        
                    for (x,y,w,h) in upper_bodies:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),3, 4, 0)
                        
                    for (x,y,w,h) in eyes:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),3, 4, 0)
                        
                    if (ret):
                        cv2.imshow('Frame',img)
                        #print(str(len(bodies)))
                        
                    if len(bodies) > 0 or len(upper_bodies) or len(eyes):  # Recognizing the whole & upper body, eyes
                        detected = detected + 1
                        print(str(detected))  # checking 
                    else:
                        nohuman = nohuman + 1
                    
                    if detected > 5 : # 녹화 시작 
                        out.write(img)
                    
                    if nohuman == 1000 : # If it's not recognized continuously, Reset!
                        a = 0
                        detected = 0
                        nohuman = 0
                        flag = 1
                        break
                        
                    if GPIO.input(14) is 0 : # if push the button, (Prevent duplication of functions)
                        cv2.destroyAllWindows()
                        flag = 1
                        break    
                        
                    if cv2.waitKey(1) == ord('q'):
                        GPIO.cleanup()   
                        break
                        
                if flag == 1: # Return to the starting line 
                    break
       
       
                #cap.release()
                cv2.destroyAllWindows()
                subprocess.run('MP4Box -add video.avi video.mp4', shell=True)  # Convert avi file to mp4 file
                kakao2()
                
               
                #initialize
                a = 0
                flag = 0
                detected = 0 
                nohuman = 0
                count = 0 
                break

    
finally:
    GPIO.cleanup()        
