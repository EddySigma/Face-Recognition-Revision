import cv2
import sys
import numpy as np





def addFace(data, img):
	noseCascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
	imHappy = cv2.imread('happy.png', -1)
	orig_mask = imHappy[:,:,3]
	orig_mask_inv = cv2.bitwise_not(orig_mask)
	imHappy = imHappy[:,:,0:3]
	origImageHeight, origImageWidth = imHappy.shape[:2]
	


	gray = cv2.cvtColor(data[0],cv2.COLOR_BGR2GRAY)
	
	roi_gray = gray[data[2]:data[2]+data[4],data[1]:data[1]+data[3]]
	roi_color = data[0][data[2]:data[2]+data[4],data[1]:data[1]+data[3]]
	nose = noseCascade.detectMultiScale(roi_gray)
	
	
	for (nx,ny,nw,nh) in nose:
		# Un-comment the next line for debug (draw box around the nose)
		#cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(255,0,0),2)

		# The mustache should be three times the width of the nose
		happyWidth =  8 * nw
		happyHeight = happyWidth * origImageHeight / origImageWidth

		# Center the mustache on the bottom of the nose
		x1 = nx - (happyWidth/4)
		x2 = nx + nw + (happyWidth/4)
		y1 = ny + nh - (happyHeight/2)
		y2 = ny + nh + (happyHeight/2)

		# Check for clipping
		if x1 < 0:
			x1 = 0
		if y1 < 0:
			y1 = 0
		if x2 > data[3]:
			x2 = data[3]
		if y2 > data[4]:
			y2 = data[4]

		# Re-calculate the width and height of the mustache image
		happyWidth = x2 - x1
		happyHeight = y2 - y1

		# Re-size the original image and the masks to the mustache sizes
		# calcualted above
		happy = cv2.resize(imHappy, (happyWidth,happyHeight), interpolation = cv2.INTER_AREA)
		mask = cv2.resize(orig_mask, (happyWidth,happyHeight), interpolation = cv2.INTER_AREA)
		mask_inv = cv2.resize(orig_mask_inv, (happyWidth,happyHeight), interpolation = cv2.INTER_AREA)

		# take ROI for mustache from background equal to size of mustache image
		roi = roi_color[y1:y2, x1:x2]

		# roi_bg contains the original image only where the mustache is not
		# in the region that is the size of the mustache.
		roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

		# roi_fg contains the image of the mustache only where the mustache is
		roi_fg = cv2.bitwise_and(happy,happy,mask = mask)

		# join the roi_bg and roi_fg
		dst = cv2.add(roi_bg,roi_fg)

		# place the joined image, saved to dst back over the original image
		roi_color[y1:y2, x1:x2] = dst

		break
	return data[0]


























 
   
