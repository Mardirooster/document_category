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

from bound import bound, standardise_rectangles, sum_bound
from categorise import categorise_histograms, match_rects_jaccard, categorise_rects
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


image = remove_lines(cv2.imread(dir_path + files[3]));
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)

invert = cv2.bitwise_not(thresh)

rects = sum_bound(invert)

for rect in rects:
	print(rect)
	image = cv2.rectangle(image,(rect[1],rect[0]),(rect[3],rect[2]),(0,255,0),2)

cv2.imshow("i",image)
cv2.waitKey(0)


categorised_rect = categorise_rects( files , directory=dir_path, save_file="rects.npy")



for category, imglist in categorised_rect.items():
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














rectangles = {}



if True:
	for f in files:
		image = cv2.imread(dir_path + f);

		image = remove_lines(image)

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

			rectangles[f] = stand


	#		cv2.imshow(f,image)
	#		cv2.waitKey(0)
	#		cv2.destroyAllWindows()
		else:
			print("error reading " + f)					

	np.save(dir_path + "rectangles.npy", rectangles)
else:
	rectangles = np.load(dir_path + "rectangles.npy")

for file, rect_list_a in rectangles.items():
	for file2, rect_list_b in rectangles.items():
		if file != file2:
			cv2.imshow(file, cv2.imread(dir_path+file))
			cv2.imshow(file2, cv2.imread(dir_path+file2))
			print(match_rects_jaccard(rect_list_a, rect_list_b))
			cv2.waitKey(0)
			cv2.destroyAllWindows()
cv2.waitKey(0)

print(rectangles)
cv2.waitKey(0)




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

