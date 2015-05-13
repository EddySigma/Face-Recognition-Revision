# Filename: FINAL_addition.py
# Description: Takes an image, resizes it and centers it on the face, 
# and adds the image over the face 

import cv2
import sys
import numpy as np

def addFace(data, img):
	noseCascade = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')
	# read the image, create the regular and inverted mask of the image
	image = cv2.imread(img, -1)
	orig_mask = image[:,:,3]
	orig_mask_inv = cv2.bitwise_not(orig_mask)
	# convert image to BGR and save the original height and width (used later for re-sizing)
	image = image[:,:,0:3]
	origImageHeight, origImageWidth = image.shape[:2]

	gray = cv2.cvtColor(data[0],cv2.COLOR_BGR2GRAY)
	roi_gray = gray[data[2]:data[2]+data[4],data[1]:data[1]+data[3]]
	roi_color = data[0][data[2]:data[2]+data[4],data[1]:data[1]+data[3]]
	nose = noseCascade.detectMultiScale(roi_gray)
	
	for (nx,ny,nw,nh) in nose:
		# make image eight times the width of the nose
		imageWidth =  8 * nw
		imageHeight = imageWidth * origImageHeight / origImageWidth
		# center image at the nose
		x1 = nx - (imageWidth/4)
		x2 = nx + nw + (imageWidth/4)
		y1 = ny + nh - (imageHeight/2)
		y2 = ny + nh + (imageHeight/2)

		# check for clipping
		if x1 < 0:
			x1 = 0
		if y1 < 0:
			y1 = 0
		if x2 > data[3]:
			x2 = data[3]
		if y2 > data[4]:
			y2 = data[4]

		# re-calculate the width and height of the image
		imageWidth = x2 - x1
		imageHeight = y2 - y1

		# re-size the original image and the masks to the image sizes
		# calculated above
		imageResized = cv2.resize(image, (imageWidth,imageHeight), interpolation = cv2.INTER_AREA)
		mask = cv2.resize(orig_mask, (imageWidth,imageHeight), interpolation = cv2.INTER_AREA)
		mask_inv = cv2.resize(orig_mask_inv, (imageWidth,imageHeight), interpolation = cv2.INTER_AREA)

		# take ROI for image from background equal to size of image
		roi = roi_color[y1:y2, x1:x2]

		# roi_bg contains the original image only where the image is not
		# in the region that is the size of the image.
		roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

		# roi_fg contains the image of the image only where the image is
		roi_fg = cv2.bitwise_and(imageResized,imageResized,mask = mask)

		# join the roi_bg and roi_fg
		dst = cv2.add(roi_bg,roi_fg)

		# place the joined image, saved to dst back over the original image
		roi_color[y1:y2, x1:x2] = dst

		break
	return data[0]


























 
   
