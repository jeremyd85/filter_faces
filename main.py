import numpy as np
import cv2
import sys
import os
import time
from imutils.video import VideoStream
from imutils.video import FPS
import imutils

CLASSIFIER = '/home/jeremy/code/C++Projects/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
FILEPATH = 'Jeremy'


def get_image_list(dir_name):
    if os.path.exists(dir_name):
        image_list = os.listdir(dir_name)
        return [os.path.join(dir_name, f) for f in image_list]
    else:
        return []


def main():

    face_cascade = cv2.CascadeClassifier(CLASSIFIER)
    image_list = get_image_list(FILEPATH)
    for i in image_list[0:1]:
        cv_img = cv2.imread(i)
        cv_grayscale_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            image=cv_grayscale_img,
            scaleFactor=1.3,
            minNeighbors=1,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow(i, cv_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(faces)

main()



# img_name = 'Jeremy/032.jpg'
# img = cv2.imread(img_name, 0)
# cv2.imshow(img_name, img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()