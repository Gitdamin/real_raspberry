## detect face and eye
# start eye recognition after press i
# show the rectangular boxes on face and text on monitor

import cv2

font = cv2.FONT_ITALIC

def faceDetect():
    eye_detect = False
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")  # 얼굴찾기 haar 파일
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml") # 눈찾기 haar 파일

    try:
        cam = cv2.VideoCapture(-1)
    except:
        print("camera loading error")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        if eye_detect:
            info = "Eye Detention ON"
        else:
            info = "Eye Detection OFF"

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3, 5)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # show the info using TEXT
        cv2.putText(frame, info, (5,15), font, 0.5, (255,0, 255),1)

        for(x,y, w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)  #사각형 범위
            cv2.putText(frame, "Detected Face", (x-5, y-5), font, 0.5, (255,255,0),2)  #얼굴찾았다는 메시지
            if eye_detect:  #눈찾기
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

        cv2.imshow("frame", frame)
        k=cv2.waitKey(30)

        # eye recognition -> on, off
        if k == ord('i'):
            eye_detect = not eye_detect
        if k == 27:
            break
    cam.release()
    cv2.destroyAllWindows()

faceDetect()
