import cv2
import cv
import numpy as np
import scipy

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouthCascade = cv2.CascadeClassifier('haarcascade_smile.xml')
happy_face = '/Users/Clarissa/Documents/SPRING_15/CST205/Face-Recognition/emojis/happy.jpeg'
#happy = cv.LoadImage(happy_face)
#cv.ShowImage("example", happy)

video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60, 60))
	count = 0
	#print 'faces:', len(faces)
	for (x,y,w,h) in faces:
		#image = cv2.resize(happy_face, (0,0), w, h)
		roi_gray = gray[y:y+(h / 2), x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		#cv2.imwrite(happy, roi_color)
		eyes = eyeCascade.detectMultiScale(roi_gray)
		y_value = y-(2*3/h)
		mouth_roi_gray = gray[y_value:y+h, x:x+w]
		mouth = mouthCascade.detectMultiScale(mouth_roi_gray)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		#print 'eyes:', len(eyes)
		for (ex, ey, ew, eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		for(mx, my, mw, mh) in mouth:
			if my >= y_value:
				cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,0,255),2)
					
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.imshow('Image', image)
		break
	
video_capture.release()
cv2.destroyAllWindows()
