import RPi.GPIO as GPIO
import time

from selenium import webdriver
import urllib

GPIO.setmode(GPIO.BCM)

pirPin = 7

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

detectednum = 0

while True:
    if GPIO.input(pirPin) == GPIO.LOW:
        detectednum += 1
        print ("Motion detected! "+str(detectednum))
        if (detectednum >= 10) :
            break

    else:
        detectednum = 0                             #연속해서 10번이상 감지되어야 조건실행 
        print ("No motion! "+str(detectednum))
        continue
        
      
    time.sleep(0.2)


    time.sleep(0.2)




while True:
    
    if (detectednum >= 10) :
    
        id = '~' #카카오톡 아이디
        pw = '~' #카카오톡 비밀번호

        KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
        ChatRoom = 'https://center-pf.kakao.com/_dLeCs/chats/4812080438129747' #카카오톡챗봇 주소
        options = webdriver.ChromeOptions()

 
        #user-agent 변경
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")
 
 
        #크롬 드라이버 로드
        driver = webdriver.Chrome('/lib/chromium-browser/chromedriver', options=options)
        driver.implicitly_wait(3)
         
 
        #카카오 메인 페이지 로드
        driver.get(KaKaoURL)
        time.sleep(3)

        driver.find_element_by_id('id_email_2').send_keys(id)
        driver.find_element_by_id('id_password_3').send_keys(pw)
        
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
        time.sleep(3)
 
  
        #채팅방 로드
        driver.get(ChatRoom)
        time.sleep(3)
        
    
        #글 작성
        driver.find_element_by_id('chatWrite').send_keys('움직임이 감지되었습니다.')  #메시지 작성
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click()
        
        time.sleep(5)
     
        driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/button').click()
        driver.find_element_by_css_selector('#kakaoWrap > div.chat_popup > div.popup_body > div > div.write_chat2 > div.write_menu > div:nth-child(1) > div.upload_btn > input').send_keys('파일경로')
        time.sleep(20) #짧은 영상 파일 전송 
        
        driver.quit()
        
        time.sleep(60)
        break
