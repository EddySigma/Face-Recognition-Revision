import sys
import cv2
import numpy as np
import thread

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouthCascade = cv2.CascadeClassifier('haarcascade_smile.xml')
smile = cv2.imread('smile.jpeg')
x_offset=y_offset=50


video_capture = cv2.VideoCapture(0)

def findEyes(gray, roi_color):
	roi_gray = gray[y:y+(h / 2), x:x+w]
	eyes = eyeCascade.detectMultiScale(roi_gray)
	for (ex, ey, ew, eh) in eyes:
		print 'eye'
		cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	return

def findMouth(mouth_roi_gray, roi_color):
	mouth = mouthCascade.detectMultiScale(mouth_roi_gray)
	for(mx, my, mw, mh) in mouth:
		if my >= y_value:
			cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,0,255),2)
	return

def findFace(frame, gray):
	
	
	eye_roi_color = frame[y:y+h, x:x+w]
	faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60, 60))
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
	try:
		thread.start_new_thread(findEyes, (gray, eye_roi_color))
	except:
		print 'Failed eye thread'
while True:
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#frame[y:y+h,x:x+w] = smile
		
		mouth_roi_color = frame[y:y+h, x:x+w]
		#eyes = eyeCascade.detectMultiScale(roi_gray)
		y_value = y-(2*3/h)
		mouth_roi_gray = gray[y_value:y+h, x:x+w]
		#mouth = mouthCascade.detectMultiScale(mouth_roi_gray)
		
		try:
			thread.start_new_thread(findEyes, (roi_gray, eye_roi_color))
		except:
			print 'Failed eye thread'
		'''
		try:
			thread.start_new_thread(findMouth, (mouth_roi_gray, mouth_roi_color))
		except:
			print 'Failed mouth thread'
		'''
		#print 'eyes:', len(eyes)
	
			
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
video_capture.release()
cv2.destroyAllWindows()
		
