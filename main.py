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



# TEMPLATE GENERATION

templates = []

for f in files:
	image = cv2.imread(dir_path + f)

	cv2.imshow(f,image)

	print("Is this a template? (y/n)")
	k = cv2.waitKey(0)
	if k == 121:
		templates.append(f)

print(templates)

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

