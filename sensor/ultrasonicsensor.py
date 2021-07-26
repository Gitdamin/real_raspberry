#기능2
import RPi.GPIO as GPIO

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
