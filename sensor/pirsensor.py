import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM) # 핀을 GPIO 핀 번호 기준으로 부름
PIR = 7  # PIR 핀을 BCM 7번에 연결
GPIO.setup(PIR, GPIO.IN, GPIO.PUD_UP) # 핀 모드 설정

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
