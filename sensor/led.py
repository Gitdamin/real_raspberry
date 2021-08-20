# LED가 5초 간격으로 자동 ON, OFF 
# 5번 반복 후 종료

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 부름

GPIO.setup(17, GPIO.OUT) # 핀의 모드를 설정합니다.

for i in range(1, 5): # i를 1부터 5까지 1씩 올리며 아래 명령을 실행합니다.
   GPIO.output(17, GPIO.HIGH) # 17번 핀을 HIGH상태로 설정합니다. LED가 켜집니다.
   sleep(1) # 1초간 기다립니다.
   GPIO.output(17, GPIO.LOW) # 17번 핀을 LOW 상태로 설정합니다. LED가 꺼집니다.
   sleep(1)
GPIO.cleanup() # GPIO 모듈의 리소스를 해제합니다.
