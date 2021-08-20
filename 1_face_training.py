## Training code ##
# detect eyes and look for each char.

import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        # extract each id only
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        eyes = detector.detectMultiScale(img_numpy)
        
        for (x,y,w,h) in eyes:
            faceSamples.append(img_numpy)
            ids.append(id)
    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# save trainer file
recognizer.save('/home/pi/Documents/face_detection/trainer/trainer.yml') 
# Print the numer of faces trained
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
