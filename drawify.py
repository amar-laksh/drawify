#!/usr/bin/env python
import cv2
import platform
import time
import numpy as np
import os
# TODO - Implement structures, logging functions and json creation.
__author__ = "Amar Lakshya"
__copyright__ = "Copyright 2016"
__credits__ = ["Amar Lakshya"]
__license__ = "CC"
__version__ = "0.2"
__maintainer__ = "AmarLakshya"
__email__ = "amar.lakshya@xaviers.edu.in"
__status__ = "Production"

area = ""
shape = " "
font = cv2.FONT_HERSHEY_SIMPLEX
camera_port = 1 
camera = cv2.VideoCapture(camera_port)
filename = "./image.png"
thres_val = 0
cv2.namedWindow('Detected Image',10000)
cv2.createTrackbar("Threshold","Detected Image",110,300,lambda x : x+1)


def find(what, contour):
	if what is "area":
		return cv2.contourArea(contour)
	elif what is "perimeter":
		return cv2.arcLength(contour, True)
	elif what is "moments":
		return cv2.moments(contour)
	elif what is "convexHull":
		return cv2.convexHull(contour)
	elif what is "minRectangle":
		rect = cv2.minAreaRect(contour)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		return box



while True:
    thres_val = cv2.getTrackbarPos("Threshold", "Detected Image")
    ret, frame = camera.read()
    capture = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    gray = cv2.flip(gray, 1)
    ret,thresh = cv2.threshold(gray, thres_val, 255, cv2.THRESH_BINARY_INV)
    im_floodfill = thresh.copy()
    h, w = thresh.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
 
    cv2.floodFill(im_floodfill,mask,(0,0),255)
    img_out = thresh | cv2.bitwise_not(im_floodfill)
    cv2.imshow("Detected Image", img_out)
    count = 0
    some, contours, heirarchy = cv2.findContours(img_out,1,2)
    frame = cv2.flip(frame, 1)
    if len(contours) != 0:
        for cnt in contours:
            area = find("area", cnt)
            M = find("moments", cnt)
            approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
            if len(approx) == 5:
                shape = "Pentagon"
                cv2.drawContours(frame,[cnt],0,255,-1)
            elif len(approx) == 3:
                shape = "Triangle"
                cv2.drawContours(frame,[cnt],0,(0,255,0),-1)
                bound = find("convexHull", cnt)
            elif len(approx) == 4:
                shape = "4-Polygon"
                cv2.drawContours(frame,[cnt],0,(0,0,255),-1)
                bound = find("minRectangle", cnt)
            elif len(approx) == 9:
                shape = "Half-Circle"
                cv2.drawContours(frame,[cnt],0,(255,255,0),-1)
            elif len(approx) > 10:
                shape = "Circle"
                cv2.drawContours(frame,[cnt],0,(0,255,255),-1)
            count = count+1
            cv2.drawContours(frame,[bound],0,(255,255,255),2)
            try:
            	cx = int(M['m10']/M['m00'])
            	cy = int(M['m01']/M['m00'])
            	cv2.circle(frame
	            	, (cx, cy)
	            	,10, (0,0,0),-1
	            	)
            except:
            	pass
    else:
        shape = ""
        print "\033c"

    cv2.putText(frame,shape,(20,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Area:"+str(area),(200,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Objects: "+str(count),(400,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Webcam",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
del(camera)
cv2.destroyAllWindows()