# change brightness - add/ sub
import cv2
import numpy as np

# call image model/ face image
src = cv2.imread('/~.jpg', cv2.IMREAD_COLOR)

# initialize
val = 10
count = 0

face_id = input('\n write your id and push the enter button => ')
char = 'mask'  # personal char.

while 1 :
    
    array = np.full(src.shape, (val, val, val), dtype=np.uint8)
    add = cv2.add(src, array)
    sub = cv2.subtract(src, array)
    val += 4
    count += 1
    if val <= 30 :
        
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + '_add' + '.' + str(count) + ".jpg", add)
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(char) + '_sub' + '.' + str(count) + ".jpg", sub)
    else :
        break
    
    
cv2.waitKey()
cv2.destroyAllWindows()