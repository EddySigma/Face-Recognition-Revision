# Filename: FINAL_webcam.py
# Description: Main file that runs the whole program. Opens all of the necessary 
# cascades to detect the face, eyes, nose, and mouth. Passes all the data to detect
# the emotion and then adds the corresponding emoji.  

import sys
import os
import cv2
import numpy as np
from multiprocessing import Process, Pipe
import _thread
from FINAL_algorithm import detectEmotion
from FINAL_addition import addFace
import datetime

## print '1'
mouthCascade = cv2.CascadeClassifier('cascades/haarcascade_smile.xml')
rightEyeCascade = cv2.CascadeClassifier('cascades/right_eye.xml')
leftEyeCascade = cv2.CascadeClassifier('cascades/left_eye.xml')
noseCascade = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')
x_offset=y_offset=50

# To kill the memory leaks when running this file, run this command
# pkill -f webcamMartyVer.py

def findRightEye(conn, data):
       # roi_color = frame[data[2]:data[2]+(data[3]/2), data[1]:data[1]+data[4]]
	eyes = rightEyeCascade.detectMultiScale(data[0])
	# print 'Right Eye:', len(eyes)
	if(len(eyes) == 0):
		conn.send(False)
		conn.close()
	else:
		conn.send(True)
                      #  # print "Rh:",h
		conn.close()

def findLeftEye(conn, data):
	#roi_color = frame[data[2]:data[2]+(data[3]/2), data[1]:data[1]+data[4]]
	eyes = leftEyeCascade.detectMultiScale(data[0])
	## print 'Left Eye:', len(eyes)
	if(len(eyes) == 0):
		conn.send(False)
		conn.close()
	else:
		conn.send(True)
                     #   # print 'Lh:', h
		conn.close()
        

def findMouth(conn, data):
    mouth = mouthCascade.detectMultiScale(data[0])
    roi_color = frame[data[2]:data[2]+(data[3]/2), data[1]:data[1]+data[4]]
    if(len(mouth) == 0):
        conn.send([0,0,0,0])
        conn.close()
    else:
        for (x, y, w, h) in mouth:
            conn.send([w,h])
            # # print "w:",w, "h:",h
            break
        conn.close()

def findFace(frame, gray):
	eye_roi_color = frame[y:y+h, x:x+w]
	faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60, 60))
	try:
		_thread.start_new_thread(findEyes, (gray, eye_roi_color))
	except:
		print ('Failed eye thread')

def saveImage(image):
	cv2.imwrite('saved/'+str(datetime.datetime.now())+'.png', image)

# The real program starts to run at this point.
if __name__ == '__main__':
    faceCascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml') # opens face data file
    video_capture = cv2.VideoCapture(0)

    video_capture.set(3,1080)
    video_capture.set(4,1024)
    video_capture.set(15,0.1)


    right_eye_parent_conn, right_eye_child_conn = Pipe()
    left_eye_parent_conn, left_eye_child_conn = Pipe() # this creates a pipe
    mouth_parent_conn, mouth_child_conn = Pipe()
    emotion_parent_conn, emotion_child_conn = Pipe()
    nose_parent_conn, nose_child_conn = Pipe()
    counter = 0
    path = None
    prepath = None
    while True:
        #parent_conn, child_conn = Pipe()
        ret, frame = video_capture.read() # get video or access camera?
        feature_data = []      
        eye_frame = []
        if (ret):       # If an invalid frame is found then stop!
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # video grayscale?
            faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60,60)) # searches video for faces

            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+(h/2), x:x+w] # Area to search for the eyes. // this is half the face frame.
                nose_roi_gray = gray[y:y+h,x:x+w]
                roi_color = frame[y:y+h,x:x+w]
                ## print 'stuff'
                mouth_roi_gray = gray[(y+h)/2:y+h,x:x+w]
                ## print mouth_roi_gray


                # thread that finds eyes
                data = [roi_gray,x,y,w,h]
                ## print data
                mouth_data = [mouth_roi_gray,x,y,w,h]

                ## print 'here'
                R = Process(target=findRightEye, args=(right_eye_child_conn, data,))
                L = Process(target=findLeftEye, args=(left_eye_child_conn, data,))
                M = Process(target=findMouth, args=(mouth_child_conn, mouth_data,))


                ## print 'here2'
                M.start()
                R.start()
                L.start()

                ## print 'here3'
                eye_frame.append(right_eye_parent_conn.recv())
                eye_frame.append(left_eye_parent_conn.recv())
                # print eye_frame
                mouth_frame = mouth_parent_conn.recv()
                ## print eye_frame
                feature_data.append(eye_frame[0])
                feature_data.append(eye_frame[1])

                feature_data.append(mouth_frame[0])
                feature_data.append(mouth_frame[1])
                feature_data.append(w)
                feature_data.append(h)
                E = Process(target=detectEmotion, args=(emotion_child_conn, feature_data))
                E.start()
                
                picture_path = emotion_parent_conn.recv()
                if(counter == 0):
                    prepath = picture_path

                if(counter == 5):
                    prepath = picture_path
                    counter = 0
                else:
                    counter += 1

                # print counter
                
                ## print picture_path
                data = [frame, x,y,w,h]
                frame = addFace(data, prepath)
                #N = Process(target=addFace, args=(nose_child_conn, data, picture_path))
                ## print 'sdonf'
                #N.start()
                # # print picture_path
                R.terminate()
                L.terminate()
                M.terminate()
                E.terminate()
                #N.terminate()
        else:
            break


        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.VideoCapture(0).release
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            saveImage(frame)
            # print 'saved'


	
cv2.VideoCapture(0).release()
cv2.destroyAllWindows()
		
