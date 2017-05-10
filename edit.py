
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


def density( image ):
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
	invert = cv2.bitwise_not(thresh)





def remove_noise( image , iterations=1):
	kernel = np.ones((2,2),np.uint8)

	for i in range(iterations):


		gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		gauss = cv2.GaussianBlur(gray_image, (5, 5), 0)
		ret,thresh = cv2.threshold(gauss,210,255,cv2.THRESH_BINARY)
		invert = cv2.bitwise_not(thresh)
		
		#invert = cv2.dilate(invert, kernel, iterations=1)

		im2, contours, hierarchy = cv2.findContours(invert,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		small_contours = []

		for c in contours:
			area = cv2.contourArea(c)
			if area < 5:
				small_contours.append(c)

		cv2.drawContours(thresh, small_contours, -1, (255,255,255), -1)
		
		mask = cv2.bitwise_not(thresh)
		blank = np.ones(mask.shape, np.uint8) * 255

		out = cv2.bitwise_and(gray_image,gray_image, blank, mask)

		return out

		
		

