## Main code [eye detection + recognize each person + send the kakao talk message to user]
# [Monitor] show both current video in front of the door and captured image when you push the button
# [Phone] send the info such as captured image and one's id to user  

import RPi.GPIO as GPIO 
from time import sleep 
import datetime
from selenium import webdriver
import urllib

#GPIO pin num setting
GPIO.setmode(GPIO.BCM) 
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down mode
GPIO.setup(17, GPIO.OUT) # set GPIO 17 as output for white led  
GPIO.setup(27, GPIO.OUT) # set GPIO 27 as output for red led  
GPIO.setup(22, GPIO.OUT) # set GPIO 22 as output for red led

hz = 75
#hz = int(hz)
red = GPIO.PWM(17, hz)    # create object red for PWM on port 17  
green = GPIO.PWM(27, hz)      # create object green for PWM on port 27   
blue = GPIO.PWM(22, hz)      # create object blue for PWM on port 22 

import numpy as np 
import cv2

# change to a larger size
def set_size(img, scale):
    return cv2.resize(img, dsize=(int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

def kakao():
    
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
    sleep(1)
          
    driver.find_element_by_id('id_email_2').send_keys(id)  # write id
    driver.find_element_by_id('id_password_3').send_keys(pw)  # write password
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()  # click the input button
    sleep(1)
        
    # personal chatroom load
    driver.get(ChatRoom)
    sleep(1)
        
    # write message
    driver.find_element_by_id('chatWrite').send_keys('초인종을 눌렀습니다.')  
    # When eye recognition and image storage are successful
    if count > 3 :   
          driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/Documents/face_detection/test_capture_03.jpg') 
            
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
            
    sleep(2)        
    driver.quit()
    sleep(1)
    exit()  # End the program
   

try: 
    count = 0  #initialize
    while 1 :
       sleep(0.5)
       if GPIO.input(14) is 0:
          print('PUSH THE BUTTON')
          # LED on
          red.start(100)   #start red led
          green.start(100) #start green led
          blue.start(100)  #start blue led
         
          now = datetime.datetime.now()  #time out 기능
          # N seconds after ringing the doorbell
          time_10 = now + datetime.timedelta(seconds =10) 
          time_5 = now + datetime.timedelta(seconds =5)  
          time_2 = now + datetime.timedelta(seconds =2)  
        
          # Use haarcascade_frontalface_default.xml file as Classifier
          eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
          cap = cv2.VideoCapture(-1)
          cap.set(3,640) # set Width
          cap.set(4,480) # set Height
          while True:
             ret, img = cap.read() 
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             now = datetime.datetime.now() 
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
             now = datetime.datetime.now()          
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
          kakao()
            
       else:
          print('NOT PUSH THE BUTTON')
            
except KeyboardInterrupt:
   pass

GPIO.cleanup()


