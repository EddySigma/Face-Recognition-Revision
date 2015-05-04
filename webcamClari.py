import sys
import cv2
import numpy as np
from multiprocessing import Process, Pipe
import thread
from emotionalAlgorithms import detectEmotion

#print '1'
mouthCascade = cv2.CascadeClassifier('haarcascade_smile.xml')
rightEyeCascade = cv2.CascadeClassifier('right_eye.xml')
leftEyeCascade = cv2.CascadeClassifier('left_eye.xml')
noseCascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_mcs_nose.xml')
x_offset=y_offset=50
# Load our overlay image: mustache.png
imgHappy = cv2.imread('faces/happy.png',-1) #need this

 
# Create the mask for the mustache
orig_mask = imgHappy[:,:,3] #need this
 
# Create the inverted mask for the mustache
orig_mask_inv = cv2.bitwise_not(orig_mask)
 
# Convert mustache image to BGR
# and save the original image size (used later when re-sizing the image)
imgHappy = imgHappy[:,:,0:3] #need this
origHappyHeight, origHappyWidth = imgHappy.shape[:2]

# To kill the memory leaks when running this file, run this command
# pkill -f webcamMartyVer.py

def findRightEye(conn, data):
       # roi_color = frame[data[2]:data[2]+(data[3]/2), data[1]:data[1]+data[4]]
	eyes = rightEyeCascade.detectMultiScale(data[0])
	#print 'Right Eye:', len(eyes)
	if(len(eyes) == 0):
		conn.send([0,0,0,0])
		conn.close()
	else:
		for (x, y, w, h) in eyes:
		        conn.send([x,y,x+w,y+h])
                      #  print "Rh:",h
		conn.close()

def findLeftEye(conn, data):
	#roi_color = frame[data[2]:data[2]+(data[3]/2), data[1]:data[1]+data[4]]
	eyes = leftEyeCascade.detectMultiScale(data[0])
	#print 'Left Eye:', len(eyes)
	if(len(eyes) == 0):
		conn.send([0,0,0,0])
		conn.close()
	else:
		for(x,y,w,h) in eyes:
			conn.send([x,y,x+w,y+h])
                     #   print 'Lh:', h
		conn.close()

def findMouth(conn, data):
	mouth = mouthCascade.detectMultiScale(data[0])
        #roi_color = frame[data[2]:data[2]+(data[3]/2), data[1]:data[1]+data[4]]
        if(len(mouth) == 0):
            conn.send([0,0,0,0])
            conn.close()
        else:
            for (x, y, w, h) in mouth:
                conn.send([x,y,x+w,y+h])
               # print "w:",w, "h:",h
                break
            conn.close()

def findFace(frame, gray):
	
	
	eye_roi_color = frame[y:y+h, x:x+w]
	faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60, 60))
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
	try:
		thread.start_new_thread(findEyes, (gray, eye_roi_color))
	except:
		print 'Failed eye thread'


# The real program starts to run at this point.
if __name__ == '__main__':
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # opens face data file
    video_capture = cv2.VideoCapture(0)

    video_capture.set(3,1080)
    video_capture.set(4,1024)
    video_capture.set(15,0.1)


    right_eye_parent_conn, right_eye_child_conn = Pipe()
    left_eye_parent_conn, left_eye_child_conn = Pipe() # this creates a pipe
    mouth_parent_conn, mouth_child_conn = Pipe()
    emotion_parent_conn, emotion_child_conn = Pipe()
    while True:
        #parent_conn, child_conn = Pipe()
        ret, frame = video_capture.read() # get video or access camera?
        feature_data = []       
        if (ret):       # If an invalid frame is found then stop!
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # video grayscale?
            faces = faceCascade.detectMultiScale(gray, 1.2, 6, minSize = (60,60)) # searches video for faces

            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) # frame for the face: blue
                roi_gray = gray[y:y+(h/2), x:x+w] # Area to search for the eyes. // this is half the face frame.
      
                roi_color = frame[y:y+h,x:x+w]
                #print 'stuff'
                mouth_roi_gray = gray[(y+h)/2:y+h,x:x+w]
                #print mouth_roi_gray
                nose = noseCascade.detectMultiScale(roi_gray)
                for (nx,ny,nw,nh) in nose:
            		# Un-comment the next line for debug (draw box around the nose)
            		#cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(255,0,0),2)
            		# The mustache should be three times the width of the nose
            			happyWidth =  6 * nw
            			happyHeight = happyWidth * origHappyHeight / origHappyWidth
 
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
            			if x2 > w:
                			x2 = w
            			if y2 > h:
                			y2 = h
 
            			# Re-calculate the width and height of the mustache image
            			happyWidth = x2 - x1
            			happyHeight = y2 - y1
 
            			# Re-size the original image and the masks to the mustache sizes
            			# calcualted above
            			happy = cv2.resize(imgHappy, (happyWidth,happyHeight), interpolation = cv2.INTER_AREA)
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
	

                # thread that finds eyes
                data = [roi_gray,x,y,w,h]
                #print data
                mouth_data = [mouth_roi_gray,x,y,w,h]

		#print 'here'
                R = Process(target=findRightEye, args=(right_eye_child_conn, data,))
		L = Process(target=findLeftEye, args=(left_eye_child_conn, data,))
                M = Process(target=findMouth, args=(mouth_child_conn, mouth_data,))
		#print 'here2'
                M.start()
                R.start()
		L.start()
		#print 'here3'
                eye_frame = right_eye_parent_conn.recv()
                eye_frame += left_eye_parent_conn.recv()
                mouth_frame = mouth_parent_conn.recv()
                #print eye_frame
                cv2.rectangle(roi_color,(eye_frame[0],eye_frame[1]),(eye_frame[2],eye_frame[3]),(0,255,0),2)
                cv2.rectangle(roi_color,(eye_frame[4],eye_frame[5]),(eye_frame[6],eye_frame[7]),(0,255,0),2)
                cv2.rectangle(roi_color,(mouth_frame[0],mouth_frame[1]),(mouth_frame[2],mouth_frame[3]),(0,255,0),2)

                if(eye_frame[1] == 0):
                    feature_data.append(False)
                else:
                    feature_data.append(True)
                if(eye_frame[4] == 0):
                    feature_data.append(False)
                else:
                    feature_data.append(True)

                feature_data.append(mouth_frame[2] - mouth_frame[0])
                feature_data.append(mouth_frame[3] - mouth_frame[1])
                feature_data.append(w)
                feature_data.append(h)
                E = Process(target=detectEmotion, args=(emotion_child_conn, feature_data))
                E.start()

                picture_path = emotion_parent_conn.recv()
               # print picture_path
                R.terminate()
                L.terminate()
                M.terminate()
                E.terminate()
        else:
            break


        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.VideoCapture(0).release
            cv2.destroyAllWindows()
            WaitKey(1)
            break


'''
while True:
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#frame[y:y+h,x:x+w] = smile
		
        #mouth_roi_color = frame[y:y+h, x:x+w]
		#eyes = eyeCascade.detectMultiScale(roi_gray)
        y_value = y-(2*3/h)
        #mouth_roi_gray = gray[y_value:y+h, x:x+w]
		#mouth = mouthCascade.detectMultiScale(mouth_roi_gray)
		
        try:
            thread.start_new_thread(findEyes, (roi_gray, eye_roi_color))
        except:
            #print 'Failed eye thread'
        
		try:
			thread.start_new_thread(findMouth, (mouth_roi_gray, mouth_roi_color))
		except:
			#print 'Failed mouth thread'
        
		##print 'eyes:', len(eyes)
			
cv2.imshow('Video', frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break '''
	
cv2.VideoCapture(0).release()
cv2.destroyAllWindows()
		
