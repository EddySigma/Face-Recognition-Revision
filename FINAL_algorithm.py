# Filename: FINAL_algorithm.py
# Description: This file holds our emotion algorithm. We are able to detect the emotion
# expressed by the user in front of the webcam.

import sys
import cv2
import numpy as np
from multiprocessing import Process, Pipe
import _thread

winky = 'faces/winky.png'
neutral = 'faces/neutral.png'
happy = 'faces/happy.png'
alien = 'faces/alien.png'
kissy = 'faces/kissy.png'


def detectEmotion(conn, data):
    # print data
    # data for right and left eye, mouth width and height, face width and height
	hasRight = data[0]
	hasLeft = data[1]
	mouth_w = data[2]
	mouth_h = data[3]
	face_w = data[4]
	face_h = data[5]
	
	if(mouth_w != 0 and mouth_h != 0):
		#print(float(face_w) / mouth_w)
		#print(float(face_h) / mouth_h)
		if(data[0] == False and data[1] == False):  # checks to see if either the left or
			#print('winky')						    # right eye are not found and sends the
			conn.send(winky)

		elif(float(face_w) / mouth_w > 3.5):  # checks for ratio between mouth and face
			#print('kissy')
			conn.send(kissy)					# and sends the kissy image

		elif(float(face_w) / mouth_w < 2.20):  # checks for ratio between mouth and face
			#print('happy')					# and sends the happy image
			conn.send(happy)

		else:
			# sends neutral if ration between face and mouth
			#print('neutral')
			conn.send(neutral)  # is normal
						# winky image
	else:
		#print ('alien')	 # sends the alien image if it doesn't recognize
		conn.send(neutral)	 # of the emotions

	conn.close()

def detectEmotion2(conn, face_features):
    # face_features should contain right/left eye, mouth width/height and face width/height
	if(face_features['mouth_width'] != 0 and face_features['mouth_height'] != 0):
		if(face_features['l_eye'] == False and face_features['r_eye'] == False): 
			# checks to see if either the left or right eye are not found and sends the wink emoji
			conn.send(winky)

		elif(float(face_features['face_width']) / face_features['mouth_width'] > 3.5):
			# checks for ratio between mouth and face and sends the kiss emoji
			conn.send(kissy)

		elif(float(face_features['face_width']) / face_features['mouth_width'] < 2.2):
			# checks for ratio between mouth and face and sends the happy emoji
			conn.send(happy)

		else:
			# sends neutral emoji if ration between face and mouth is between 2.2 and 3.5
			conn.send(neutral)
	else:
		# sends the alien image if a face is recognized but data is out of range of the expected
		conn.send(alien)

	conn.close()