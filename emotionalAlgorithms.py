import sys
import cv2
import numpy as np
from faceAddition import addFace
from multiprocessing import Process, Pipe
import thread

winky = 'faces/winky.png'
neutral = 'faces/neutral.png'
happy = 'faces/happy.png'
alien = 'faces/alien.png'
#glasses = 'faces/glasses.png'
#tongue = 'faces/tongue.png'
#cheesy = 'faces/cheesy.png'


def detectEmotion(conn, data):
   # print data
    hasRight = data[0]
    hasLeft = data[1]
    mouth_w = data[2]
    mouth_h = data[3]
    face_w = data[4]
    face_h = data[5]
   # if(mouth_w != 0 and mouth_h != 0):
    #    print 'ratio', float(face_w) / mouth_w

    if(hasRight == False or hasLeft == False):
        print 'winky'
        addFace(winky)
    
    elif(mouth_w != 0 and mouth_h != 0):
        if(float(face_w) / mouth_w < 2.20):
            print 'smile!'
            addFace(happy)
        else:
            print 'neutral'
            addFace(neutral)
    else:
        print 'ALIEN!'
        addFace(neutral)
    conn.send(happy)
    sleep(25)
    conn.close()
