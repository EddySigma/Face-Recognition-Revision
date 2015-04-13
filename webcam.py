import sys
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60, 60))
	for (x,y,w,h) in faces:
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		eyes = eyeCascade.detectMultiScale(roi_gray)
		for (ex, ey, ew, eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
video_capture.release()
cv2.destroyAllWindows()
		
