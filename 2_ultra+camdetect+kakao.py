from selenium import webdriver
import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
import time # time 함수 사용을 위한 라이브러리 불러오기
import picamera
import datetime

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 부름

TRIG = 18 # TRIG 핀을 BCM 18번에 연결
ECHO = 24 # ECHO 핀을 BCM 24번에 연결
GPIO.setup(TRIG, GPIO.OUT) # 핀 모드 설정
GPIO.setup(ECHO, GPIO.IN) # 핀 모드 설정

PIR = 7  # PIR 핀을 BCM 7번에 연결
GPIO.setup(PIR, GPIO.IN, GPIO.PUD_UP) # 핀 모드 설정

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

    distance = ( distance1 + distance2 + distance3 + distance4 + distance5 + distance6 + distance7 + distance8 + distance9 + distance10 ) / 10
    #정밀도를 높이기 위해 1초마다 거리를 측정하여 10초동안의 평균거리 계산
    
    print(str(distance))
    
    return distance

def pirmeasure(): # PIR 센서로 움직임 측정하는 함수
    while True:
        if GPIO.input(PIR) == GPIO.LOW:
            detectednum += 1
            print ("Motion detected! "+str(detectednum))
            if (detectednum >= 10) : #연속해서 10번이상 감지되어야 조건실행 
                break

        else:
            detectednum = 0             
            print ("No motion!")
            continue

    return detectednum


def record(): # 파이카메라로 영상 녹화하는 함수
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H:%M:%S')
    camera.start_recording(output = filename + '.h264') #h.264 코덱
    camera.wait_recording(5)
    camera.stop_recording()

def login(): # 카카오톡 챗봇으로 로그인 하는 함수
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

a = 0 # 일정 거리 이내에 사람이 감지된 횟수

try:
    while True:

        distance = measure_average()
        time.sleep(1)
        if (distance <= 30) :
            a = a+1 # 일정 거리 이내에 사람이 감지되면 횟수를 1씩 증가시킴
            if (a >= 10) : 
                pirmeasure()
                #record()
                login()
                driver.find_element_by_id('chatWrite').send_keys('움직임이 감지되었습니다.') # 메세지 작성
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[2]/form/fieldset/button').click() # 메세지 전송 버튼
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/button').click() # 파일 업로드 버튼
                driver.find_element_by_css_selector('#kakaoWrap > div.chat_popup > div.popup_body > div > div.write_chat2 > div.write_menu > div:nth-child(1) > div.upload_btn > input').send_keys('파일경로')
                # 짧은 영상 파일 전송 
                time.sleep(20) 
                driver.quit()
                time.sleep(60)
                a = 0
        else:
            a = 0
    
finally:
    GPIO.cleanup()
    
        

