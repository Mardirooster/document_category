#file handling imports
import sys
import os
from os import listdir
from os.path import isfile, join
#opencv imports
import cv2
import numpy as np


dir_path = "C:\\Unnamed\\scripts\\test_images\\"
files = [f for f in listdir(dir_path) if f.endswith(".png")]

image = cv2.imread(dir_path + '0109-1.png')

gray_image = 255*(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')

cv2.imshow('Output', gray_image)
k = cv2.waitKey(0)
cv2.destroyAllWindows()
kernel = np.ones((5,5),np.uint8)

surf = cv2.xfeatures2d.SURF_create(1000)
surf.setUpright(True)

gray_image = cv2.erode(gray_image,kernel,iterations=1)
kp1, des1 = surf.detectAndCompute(gray_image,None)
img2 = cv2.drawKeypoints(gray_image,kp1,None,(255,0,0),4)
cv2.imshow('Output', img2)
k = cv2.waitKey(0)
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)


for f in files:
	image = cv2.imread(dir_path + f)

	gray_image1 = 255*(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')
	# se1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
	# se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
	# mask = cv2.morphologyEx(invert, cv2.MORPH_CLOSE, se1)
	# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)
	gray_image1 = cv2.erode(gray_image1,kernel,iterations=1)
	kp2, des2 = surf.detectAndCompute(gray_image1,None)
	print(des1)
	print(des2)
	matches = bf.match(des1,des2)
	matches = sorted(matches, key = lambda x:x.distance)
	img3 = gray_image
	img3 = cv2.drawMatches(gray_image,kp1,gray_image1,kp2,matches[:200], flags=2, outImg=img3)

	cv2.imshow('Output', img3)
	orb = cv2.ORB_create()
	k = cv2.waitKey(0)
	print(k)
	if k == 32: break
	cv2.destroyAllWindows()