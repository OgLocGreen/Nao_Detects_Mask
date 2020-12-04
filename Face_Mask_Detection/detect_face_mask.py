import os
import sys

path = os.getcwd() + "/numpy/"
sys.path.append(os.path.abspath(path))
import numpy as np


path = os.getcwd() + "/cv2/"
sys.path.append(os.path.abspath(path))
import cv2

import random


def detection(pic=None):
    
    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    #print(os.getcwd() +'/Face_Mask_Detection/data/xml/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(os.getcwd() +'/Face_Mask_Detection/data/xml/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(os.getcwd() +'/Face_Mask_Detection/data/xml/haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier(os.getcwd() +'/Face_Mask_Detection/data/xml/haarcascade_mcs_mouth.xml')
    upper_body = cv2.CascadeClassifier(os.getcwd() +'/Face_Mask_Detection/data/xml/haarcascade_upperbody.xml')



    # Adjust threshold value in range 80 to 105 based on your light.
    bw_threshold = 80

    # User message
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (30, 30)
    weared_mask_font_color = (255, 255, 255)
    not_weared_mask_font_color = (0, 0, 255)
    thickness = 2
    font_scale = 1
    weared_mask = "Thank You for wearing MASK"
    not_weared_mask = "Please wear MASK to defeat Corona"

    text = 0
    # Get individual frame
    try: 
        img = pic
    except:
        img = cv2.imread("/home/nao/recordings/cameras/image.jpg")

    # Flip the Image
    img = cv2.flip(img,1)
    # Convert Image into gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Face prediction for black and white
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)


    if(len(faces) == 0 and len(faces_bw) == 0):
        #no face found
        text = 0
    elif(len(faces) == 0 and len(faces_bw) == 1):
        #waring a mask
        text = 1
    else:
        # Draw rectangle on gace
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]


            # Detect lips counters
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
        # Face detected but Lips not detected which means person is wearing mask
        if(len(mouth_rects) == 0):
            #wearing a mask
            text = 1
        else:
            for (mx, my, mw, mh) in mouth_rects:

                if(y < my < y + h):
                    # Face and Lips are detected but lips coordinates are within face cordinates which `means lips prediction is true and
                    # person is not waring mask
                    text = 2
                    break

    return text

    cap.release()
    cv2.destroyAllWindows()