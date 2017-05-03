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

CATEGORY_FILE = 'category.npy'

MIN_CORRELATION = 0.09
#MIN_CORRELATION = 150000
COMPARE_METHODS = [cv2.HISTCMP_CORREL,cv2.HISTCMP_CHISQR,cv2.HISTCMP_INTERSECT,cv2.HISTCMP_BHATTACHARYYA] 
COMPARE_METHOD = COMPARE_METHODS[0]

histograms = {}

categorised_hist = {}

print(sys.argv)
if(len(sys.argv) < 2):

	#get current directory
	dir_path = os.path.dirname(os.path.realpath(__file__))

	templates = []

	template_histograms = {}

	for t in templates:
		image = cv2.imread(t)
		blur = cv2.blur(image,(10,10))
		gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
		template_histograms[t] = cv2.calcHist([gray_image],[0],None,[256],[0,256])

	pth = os.getcwd()

	files = [f for f in listdir(dir_path) if f.endswith(".png")]

	#print(files)


	#categorise based on histogram

	run = 0
	run = int(input("1 to run hist categorisation, any other key uses results from previous session "))


	if run==1:
		for f in files:
			image = cv2.imread(f)
			blur = cv2.blur(image,(10,10))
			gray_image = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
			hist = cv2.calcHist([gray_image],[0],None,[256],[0,256])

			max_diff = ["",0]
			for curr,h in template_histograms.items():
				diff = cv2.compareHist(h, hist, COMPARE_METHOD)
				if diff > max_diff[1]:
					max_diff = [curr, diff]

					
			if max_diff[1] < MIN_CORRELATION:
				template_histograms[f] = hist
				categorised_hist[f] = [f]
			else:
				categorised_hist[max_diff[0]].append(f)


		np.save(CATEGORY_FILE, categorised_hist)
	else:
	 	categorised_hist = np.load(CATEGORY_FILE).item()

	#show histogram categories

	run = 0
	run = int(input("1 to view results, any other key skips... "))

	if run==1:
		for category, imglist in categorised_hist.items():
			print(str(len(imglist)))

			count = 0
			for i in imglist:
				image = cv2.imread(i)
				cv2.imshow(i,image)
				count += 1
				if count%20 == 0:
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				if count > 100:
					cv2.destroyAllWindows()
					break
			
			cv2.waitKey(0)

			cv2.destroyAllWindows()



	#new categorisation type!
	run = 0
	print("select subsection for further categorisation:")
	for category, imglist in categorised_hist.items():
		print(category + " : " + str(len(imglist)) + " items.")


	#select category to perform further filtering on
	while True:
		try:
			category = input("enter category :")
			subcategory = categorised_hist[category]
			break
		except:
			print("not a valid category")

else:
	categorised_hist = np.load(CATEGORY_FILE).item()
	category = sys.argv[1]
	subcategory = categorised_hist[category]


for f in subcategory:
	image = cv2.imread(f);
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)

	invert = cv2.bitwise_not(thresh)
	print(invert)

	canny = cv2.Canny(gray_image,50,150,apertureSize = 3)
	cv2.imshow(f,canny)
	minLineLength = 1
	maxLineGap = 20
	lines = cv2.HoughLinesP(invert,1,np.pi/180,100,minLineLength,maxLineGap)

	print(lines)
	cv2.waitKey(0)
	if lines is not None:
		for [line] in lines:
			cv2.line(image,(line[0],line[1]),(line[2],line[3]),(255,255,255),2)
	
	cv2.imshow(f,image)

	img = cv2.bitwise_not(thresh)
	#cv2.imshow(f,img)

	kernel = np.ones((1,1), np.uint8)

	img = cv2.erode(img,kernel,iterations=1)
	img = cv2.dilate(img,kernel,iterations=2)
	

	#cv2.imshow(f,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
	histograms[f] = hist

def bound( img ):
	rectangles = []

	cur_rectangle = []
	for row_index,row in enumerate(img):
		for column_index,pixel in enumerate(row):
			if img[row_index][column_index]:
				curr_rectangle = [[row_index, column_index]]

				for row_offset,row in enumerate(img[row_index:-1]):
					