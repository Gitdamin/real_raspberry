## detect motion

import RPi.GPIO as GPIO # GPIO를 이용하기 위한 라이브러리 불러오기

GPIO.setmode(GPIO.BCM) # 핀을 BCM 번호 기준으로 부름

GPIO.setup(6, GPIO.IN) # 핀을 입력 모드로 설정합니다.

try: # 키보드 인터럽트 예외처리
   while True :
      i = GPIO.input(6) # 센서값을 입력받습니다.
      if i == 0: # 움직임 감지 유무를 판단합니다.
           print("움직임이 감지되었습니다.")

except KeyboardInterrupt:
   pass

GPIO.cleanup()
