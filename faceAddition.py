import cv2
import sys
import numpy as np

noseCascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

def addFace(data, img):
	print 'suff'
	nose = noseCascade.detectMultiScale(data[0])
	# Load our overlay image: img
	image = cv2.LoadImage('/home/idk/code/cst/Face-Recognition/faces/happy.png',-1)
	print 'image',image
	cv2.imshow('image', image)
 
	# Create the mask for the image
	orig_mask = image[:,:,3] #need this
 
	# Create the inverted mask for the image
	orig_mask_inv = cv2.bitwise_not(orig_mask)
 
	# Convert image to BGR and save the original image size (used later when re-sizing the image)
	image = image[:,:,0:3] #need this
	origImageHeight, origImageWidth = image.shape[:2]
	print 'nose', nose
	for (nx,ny,nw,nh) in nose:
		print nose
		# Un-comment the next line for debug (draw box around the nose)
		cv2.rectangle(data[0],(nx,ny),(nx+nw,ny+nh),(200,0,200),2)
		# The image should be eight times the width of the nose
		imageWidth = 8 * nw
		imageHeight = imageWidth * origImageHeight / origImageWidth
 		# Center the image on the bottom of the nose
 		x1 = nx - (imageWidth/4)
 		x2 = nx + nw + (imageWidth/4)
 		y1 = ny + nh - (imageHeight/2)
 		y2 = ny + nh + (imageHeight/2)
 		# Check for clipping
		'''
 		if x1 < 0:
 			x1 = 0
 		if y1 < 0:
 			y1 = 0
    	if x2 > w:
    	    x2 = w
    	if y2 > h:
    		y2 = h
		'''
 		# Re-calculate the width and height of the image
 		imageWidth = x2 - x1
 		imageHeight = y2 - y1
 		# Re-size the original image and the masks to the image sizes
 		# calculated above
 		image_resized = cv2.resize(image, (imageWidth,imageHeight), interpolation = cv2.INTER_AREA)
 		mask = cv2.resize(orig_mask, (imageWidth,imageHeight), interpolation = cv2.INTER_AREA)
 		mask_inv = cv2.resize(orig_mask_inv, (imageWidth, imageHeight), interpolation = cv2.INTER_AREA)
 	
 		# take ROI for image from background equal to size of mustache image
 		roi = data[0][y1:y2, x1:x2]
 		# roi_bg contains the original image only where the mustache is not
 		# in the region that is the size of the mustache.
 		roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
 		# roi_fg contains the image of the mustache only where the mustache is
 		roi_fg = cv2.bitwise_and(image_resized,image_resized,mask = mask)
 		# join the roi_bg and roi_fg
 		dst = cv2.add(roi_bg,roi_fg)
 		# place the joined image, saved to dst back over the original image
 		data[0][y1:y2, x1:x2] = dst
		#conn.close()
 
   
