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

from bound import bound, standardise_rectangles
from categorise import categorise_histograms
from edit import remove_lines

CATEGORY_FILE = 'category.npy'

MIN_CORRELATION = 0.09
#MIN_CORRELATION = 150000
COMPARE_METHODS = [cv2.HISTCMP_CORREL,cv2.HISTCMP_CHISQR,cv2.HISTCMP_INTERSECT,cv2.HISTCMP_BHATTACHARYYA] 
COMPARE_METHOD = COMPARE_METHODS[0]

histograms = {}

categorised_hist = {}




# NOTE: a categorisation is of the form { category : [file_name, file_name, file_name], ... }



#dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = "C:\\Unnamed\\scripts\\test_images\\"
files = [f for f in listdir(dir_path) if f.endswith(".png")]

rectangles = {}
for f in files:
	image = cv2.imread(dir_path + f);

	image = remove_lines(image)
	
	#cv2.imshow(f,image)
	#cv2.waitKey(0)
#	img = cv2.bitwise_not(thresh)
	#cv2.imshow(f,img)

#	kernel = np.ones((1,1), np.uint8)

#	img = cv2.erode(img,kernel,iterations=1)
#	img = cv2.dilate(img,kernel,iterations=2)
	

#	cv2.imshow(f,img)
#	cv2.waitKey(0)
#	cv2.destroyAllWindows()

	if image is not None:
		gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)

		invert = cv2.bitwise_not(thresh)
	#	print(invert)
		#test = bound(invert)
		#cv2.imshow(f,test)
		#cv2.waitKey(0)
		bounds = bound(invert, 10)
		stand = standardise_rectangles(bounds)
		for rect in stand:
			print(rect)
			image = cv2.rectangle(image,(0,0),(rect[0],rect[1]),(0,255,0),2)

		rectangles[f] = bounds


		cv2.imshow(f,image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	else:
		print("error reading " + f)					


def match_rects( rects_a_param, rects_b_param , min_match=0.5):
	rects_a = list(rects_a_param)
	rects_b = list(rects_b_param)
	matches = 0

	for rect in rects_a:
		match = [0];
		for rect_comp in rects_b:
			curr_match_x = rect[0]/rect_comp[0] if rect_comp[0] > rect[0] else rect_comp[0]/rect[0]
			curr_match_y = rect[1]/rect_comp[1] if rect_comp[1] > rect[1] else rect_comp[1]/rect[1]
			if (curr_match_y * curr_match_x) > match[0]:
				match = [curr_match_y * curr_match_x, rect_comp]

		if match > min_match:
			rects_a.remove(rect)
			rects_b.remove(match[1])
			matches += 1

	print(rects_a)
	print(rects_b)
	print(matches)






for file, rect_list_a in rectangles.items():
	for file2, rect_list_b in rectangles.items():
		match_rects(rect_list_a, rect_list_b)


print(rectangles)
cv2.waitKey()






print(sys.argv)
if(len(sys.argv) < 2):

	template_histograms = {}

	pth = os.getcwd()

	files = [f for f in listdir(dir_path) if f.endswith(".png")]

	print(files)


	#categorise based on hist

	categorised_hist = categorise_histograms( files , directory=dir_path)
	print(categorised_hist)

	#np.save(CATEGORY_FILE, categorised_hist)

	#show histogram categories

	for category, imglist in categorised_hist.items():
		print(str(len(imglist)))

		count = 0
		for i in imglist:
			image = cv2.imread(dir_path + i)
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
	# print("select subsection for further categorisation:")
	# for category, imglist in categorised_hist.items():
	# 	print(category + " : " + str(len(imglist)) + " items.")


	# #select category to perform further filtering on
	# while True:
	# 	try:
	# 		category = input("enter category :")
	# 		subcategory = categorised_hist[category]
	# 		break
	# 	except:
	# 		print("not a valid category")

else:
	categorised_hist = np.load(CATEGORY_FILE).item()
	category = sys.argv[1]
	subcategory = categorised_hist[category]


#for f in subcategory:

