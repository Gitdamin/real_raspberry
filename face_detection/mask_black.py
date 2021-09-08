# 마스크 삽입 코드 - black mask
import cv2
import numpy as np

# face 분류기 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# 가면 영상
face_mask = cv2.imread('/home/pi/Documents/face_detection/mask.jpg')
#cv2.imshow('test',face_mask)
h_mask, w_mask = face_mask.shape[:2]

if face_cascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

#cv2.imshow('Captured Image', img_who)
scaling_factor = 1

while True:
    
    # 사람의 정면 이미지 
    frame = cv2.imread('/home/pi/Documents/face_detection/image4.jpg', 1)
    frame = cv2.resize(frame, None,fx=scaling_factor,fy=scaling_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_rects = face_cascade.detectMultiScale(gray, 1.2, 3)
   
    for (x, y, w, h) in face_rects:
        
        if h > 0 and w > 0:

            x = int(x-w*0.1)
            y = int(y + h*0.16)
            w = int(1.25 * w)
            h = int(1.25 * h)
            
          
            # 사람의 얼굴 
            frame_roi = frame[y:y + h, x:x + w]
          
            face_mask_small = cv2.resize(face_mask, (w, h), interpolation=cv2.INTER_AREA)
            
            gray_mask = cv2.cvtColor(face_mask_small, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray_mask, 247, 255, cv2.THRESH_BINARY_INV)
            #cv2.imshow('gray_mask', gray_mask)
            #cv2.imshow('mask', mask)
        mask_inv = cv2.bitwise_not(mask)
        masked_face = cv2.bitwise_and(face_mask_small, face_mask_small, mask=mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)
        
        #cv2.imshow('masked_face', masked_face)
        #cv2.imshow('masked_frame', masked_frame)
        
        frame[y:y + h, x:x + w] = cv2.add(masked_face, masked_frame)
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Face Detector', gray)
    cv2.imwrite("/home/pi/Documents/face_detection/" + "mask_success.jpg", gray)
    c = cv2.waitKey(1)
    if c == 27:
        break
cap.release()
cv2.destroyAllWindows()
