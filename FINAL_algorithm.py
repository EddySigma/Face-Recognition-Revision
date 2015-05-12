import sys
import cv2
import numpy as np
from multiprocessing import Process, Pipe
import thread

winky = 'faces/winky.png'
neutral = 'faces/neutral.png'
happy = 'faces/happy.png'
alien = 'faces/alien.png'
kissy = 'faces/kissy.png'


def detectEmotion(conn, data):
   
    print data
    hasRight = data[0]
    hasLeft = data[1]
    mouth_w = data[2]
    mouth_h = data[3]
    face_w = data[4]
    face_h = data[5]
    
    

    if(mouth_w != 0 and mouth_h != 0):
	    print float(face_w) / mouth_w
	    print float(face_h) / mouth_h
		
	    if(float(face_w) / mouth_w < 2.20):
			print 'happy'
			conn.send(happy)
	    if(float(face_w) / mouth_w > 3.40):
	        conn.send(kissy)
	    else:
			print 'neutral'
			conn.send(neutral)
    elif(data[0] == False or data[1] == False):
        print 'winky'
        conn.send(winky)
    else:
		print 'alien'
		conn.send(alien)
    conn.close()

