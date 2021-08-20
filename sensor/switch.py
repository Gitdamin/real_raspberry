## print LOW when push the button

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기
from time import sleep # time 함수 사용을 위한 라이브러리 불러오기

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 설정

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 핀을 풀 다운 모드로 설정

try: # 키보드 인터럽트 예외처리
   while 1 :
       sleep(0.5)
       if GPIO.input(18) is 1:
          print('Input was HIGH')
       else:
          print('Input was LOW')

except KeyboardInterrupt:
   pass

GPIO.cleanup()
