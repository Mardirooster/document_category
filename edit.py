
#opencv imports
import cv2
import numpy as np



def remove_lines( image ):
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
	canny = cv2.Canny(gray_image,50,150,apertureSize = 3)
	invert = cv2.bitwise_not(thresh)

	minLineLength = 1
	maxLineGap = 20
	lines = cv2.HoughLinesP(invert,1,np.pi/180,100,minLineLength,maxLineGap)

	cv2.waitKey(0)
	if lines is not None:
		for [line] in lines:
			cv2.line(image,(line[0],line[1]),(line[2],line[3]),(255,255,255),2)

	return image