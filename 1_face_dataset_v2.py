## Data set code ##
# wearing glasses v1, 2, black mask  &  change brightness
# special case #

import cv2
import numpy as np

# face 분류기 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# call face mask
face_mask = cv2.imread('/home/pi/Documents/face_detection/~.jpg')
#cv2.imshow('test',face_mask)
h_mask, w_mask = face_mask.shape[:2]

if face_cascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

face_id = input('\n write your id and push the enter button => ')
char = 'mask'  # personal characteristic

while True:
    
    # call outsider face (model) image 
    frame = cv2.imread('/home/pi/Documents/face_detection/~.jpg', 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_rects = face_cascade.detectMultiScale(gray, 1.2, 3)
   
    for (x, y, w, h) in face_rects:
        
        if h > 0 and w > 0:
   
        # glasses version1
            x = int(x+w*0.13)
            y = int(y + h*0.28)
            w = int(0.73* w)
            h = int(0.3* h) 

        # glasses version2
        ''' x = int(x-w*0.1)
            y = int(y + h*0.03)
            w = int(1.2* w)
            h = int(0.8* h) '''

        # wearing mask _ blask version 
        ''' y = int(y + h*0.2) '''

          
            frame_roi = frame[y:y + h, x:x + w]
          
            face_mask_small = cv2.resize(face_mask, (w, h), interpolation=cv2.INTER_AREA)
            
            gray_mask = cv2.cvtColor(face_mask_small, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray_mask, 240, 255, cv2.THRESH_BINARY_INV)
           
        mask_inv = cv2.bitwise_not(mask)
        masked_face = cv2.bitwise_and(face_mask_small, face_mask_small, mask=mask)
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)
       
        frame[y:y + h, x:x + w] = cv2.add(masked_face, masked_frame)
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # general image
    cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + ".0.jpg", gray)
    src = cv2.imread('dataset/User.'+ str(face_id) + '.' + str(char) + '.0.jpg', cv2.IMREAD_COLOR)
   
    # initialize 
    val = 10  
    count = 0
    
    while 1 :
    
        array = np.full(src.shape, (val, val, val), dtype=np.uint8)
        #num += 1
        add = cv2.add(src, array)
        sub = cv2.subtract(src, array)
        val += 4
        count += 1
        if val <= 30 :
        
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + '_add' + '.' + str(count) + ".jpg", add)
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + '_sub' + '.' + str(count) + ".jpg", sub)
        else :
            exit()
    
    
cv2.waitKey()
cv2.destroyAllWindows()
    
