#초음파 센서를 사용해 거리 측정
#10cm이하에 장애물이 있을 시 led on, print distance

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
import time # time 함수 사용을 위한 라이브러리 불러오기

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 부름

TRIG = 18 # TRIG 핀을 BCM 18번에 연결
ECHO = 24 # ECHO 핀을 BCM 24번에 연결


GPIO.setup(TRIG, GPIO.OUT) # 핀의 모드를 설정합니다.
GPIO.setup(ECHO, GPIO.IN) # 핀의 모드를 설정합니다.
GPIO.setup(17, GPIO.OUT) #  led


try: # 키보드 인터럽트 예외처리
  while True :
     GPIO.output(TRIG, GPIO.HIGH)
     time.sleep(0.00001) # 10 us동안 HIGH 신호 출력
 
     GPIO.output(TRIG, GPIO.LOW)
 
     startTime = time.time() # 시작 시간 선언
     stopTime = time.time() # 종료 시간 선언
 
     while GPIO.input(ECHO) == 0: # ECHO 핀이 LOW가 아니면
        startTime = time.time() # startTime에 현재시간 저장
 
     while GPIO.input(ECHO) == 1: # ECHO 핀이 HIGH가 아니면
        stopTime = time.time() # stopTime에 현재시간 저장
 
     timeDelta = stopTime - startTime # 걸린 시간 측정
     distance = (timeDelta * 34400) / 2 # 시간을 거리값으로 환산
     
     if distance < 10 :
         GPIO.output(17, GPIO.HIGH)
         print('led on')
         time.sleep(1)
     else :
         GPIO.output(17, GPIO.LOW)  
  
     print(distance)
     time.sleep(1)

except KeyboardInterrupt:
   pass


GPIO.cleanup()