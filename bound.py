#file handling imports
import sys
import os
from os import listdir
from os.path import isfile, join
#opencv imports
import cv2
import numpy as np

import pickle
from matplotlib import pyplot as plt

min_size = 5

def expand( rect , img , border):
	x1,y1,x2,y2 = rect

	for y_offset, row in enumerate(img[y1+1:y2+border]):
#		print(row)
		for x_offset, pixel in enumerate(row[x1-border:x1-1]):
			if pixel:
				y = y1+1 + y_offset
				x = x1-border + x_offset

				if y > y2:
					y2 = y

				return [x,y1,x2,y2]

	for y_offset, row in enumerate(img[y2+1:y2+border]):
		for x_offset, pixel in enumerate(row[x1:x2]):
			if pixel:
				y = y2+1 + y_offset
				x = x1 + x_offset

				return [x1,y1,x2,y]

	for y_offset, row in enumerate(img[y1:y2+border]):
		for x_offset, pixel in enumerate(row[x2+1:x2+border]):
			if pixel:
				y = y1 + y_offset
				x = x2+1 + x_offset

				if y > y2:
					y2 = y

				return [x1,y1,x,y2]

	return rect

def in_rect(point, rect):
	px,py = point
	rx1,ry1,rx2,ry2 = rect
	return px >= rx1 and px <= rx2 and py >= ry1 and py <= ry2  

def in_rects( point, rects):
	for rect in rects:
		if in_rect(point, rect):
			return True;
	return False


# return rectangles surrounding areas on document
def bound( img , border=3):
	rectangles = []

	cur_rectangle = []

	for y, row in enumerate(img):
		for x, pixel in enumerate(row):
			if pixel and not in_rects((x,y),rectangles):
				cur_rectangle = [x,y,x,y]

				#print("found corner! ", x,y)
				while True:
					new_rect = expand( cur_rectangle, img, border)
					if cur_rectangle == new_rect:
						break
					else:
						cur_rectangle = new_rect

				x1,y1,x2,y2 = cur_rectangle

				if (x2-x1 > min_size) and (y2-y1 > min_size):
					rectangles.append(cur_rectangle)

	return rectangles




#dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = "C:\\Unnamed\\scripts\\test_images\\"
files = [f for f in listdir(dir_path) if f.endswith(".png")]



for f in files:
	image = cv2.imread(dir_path + f);
	if image is not None:
		gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)

		invert = cv2.bitwise_not(thresh)
	#	print(invert)

		bounds = bound(invert, 10)
		for rect in bounds:
			image = cv2.rectangle(image,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)

		cv2.imshow(f,image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	else:
		print("error reading " + f)



#for rect in bounds:
#	invert = cv2.rectangle(invert,)