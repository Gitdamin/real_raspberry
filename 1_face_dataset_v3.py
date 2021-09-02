# Control brightness - add/ sub

import cv2
import numpy as np

src = cv2.imread('/home/pi/Documents/face_detection/mask_success.jpg', cv2.IMREAD_COLOR)
#num = 1
val = 20
count = 0
face_id = input('\n write your id and push the enter button => ')
char = 'mask'
while 1 :
    
    #src = cv2.imread('/home/pi/Documents/face_detection/image' + str(num) + '.jpg', cv2.IMREAD_COLOR)
    array = np.full(src.shape, (val, val, val), dtype=np.uint8)
    #num += 1
    add = cv2.add(src, array)
    sub = cv2.subtract(src, array)
    val += 10
    count += 1
    if val <= 80 :
        
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + '_add' + '.' + str(count) + ".jpg", add)
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + '_sub' + '.' + str(count) + ".jpg", sub)
    if val > 100 :
        break
    
    
cv2.waitKey()
cv2.destroyAllWindows()