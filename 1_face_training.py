#딥 러닝을 활용한 얼굴 판별기 ##학습용 코드##
#사람의 눈을 인식하고 저장하여 스스로 학습한다.
#시간이 오래 소요됨 

import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
#얼굴 인식 
#detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#눈 인식 
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        #사용자의 이름 저장과정 
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        eyes = detector.detectMultiScale(img_numpy)
        #사람의 눈 학습 
        for (x,y,w,h) in eyes:
            faceSamples.append(img_numpy)
            ids.append(id)
    return faceSamples,ids
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
#다음의 위치에 저장 
recognizer.save('/home/pi/Documents/face_detection/trainer/trainer.yml') 
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
