import sys
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouthCascade = cv2.CascadeClassifier('Mouth.xml')

video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60, 60))
	count = 0
	#print 'faces:', len(faces)
	for (x,y,w,h) in faces:
		roi_gray = gray[y:y+(h / 2), x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		eyes = eyeCascade.detectMultiScale(roi_gray)
		roi_gray = gray[h / 3:y+h, x:x+w]
		mouth = mouthCascade.detectMultiScale(roi_gray)
		#print 'eyes:', len(eyes)
		for (ex, ey, ew, eh) in eyes:
			for(mx, my, mw, mh) in mouth:
				if(len(eyes) / 2 <= len(faces)):
					cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,255,0),2)
					cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
					count += 1
					print 'FOUND A FULL FACE', count
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
video_capture.release()
cv2.destroyAllWindows()
		
