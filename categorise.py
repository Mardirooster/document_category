#opencv imports
import cv2
import numpy as np
#file handling imports
import sys
import os
from edit import remove_lines
from bound import bound, standardise_rectangles

def categorise_histograms( files , correlation=0.09 , compare_method=cv2.HISTCMP_CORREL, directory=".\\", save_file = "", load_file = ""):


	template_histograms = {}
	categorised_hist = {}
	
	if not load_file:
		for f in files:
			print(f)
			image = cv2.imread(directory + f)
	#		print(image)
			blur = cv2.blur(image,(10,10))
			gray_image = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
			hist = cv2.calcHist([gray_image],[0],None,[256],[0,256])

			max_diff = ["",0]
			for curr,h in template_histograms.items():
				diff = cv2.compareHist(h, hist, compare_method)
				if diff > max_diff[1]:
					max_diff = [curr, diff]

					
			if max_diff[1] < correlation:
				template_histograms[f] = hist
				categorised_hist[f] = [f]
			else:
				categorised_hist[max_diff[0]].append(f)
	else:
		categorised_hist = np.load(directory + load_file)
	if save_file:
		np.save(directory + save_file, categorised_hist)
	return categorised_hist		



def match_rects_jaccard( rects_a_param, rects_b_param , min_match_ratio=0.5, min_number_of_matches_ratio=0.5):
	print("hi")
	rects_a = list(rects_a_param)
	rects_b = list(rects_b_param)
	matches = 0
	union = 0

	for rect in rects_a:
		match = [0];
		for rect_comp in rects_b:
			#print(rect)
			#print(rect_comp)
			curr_match_x = rect[0]/rect_comp[0] if rect_comp[0] > rect[0] else rect_comp[0]/rect[0]
			curr_match_y = rect[1]/rect_comp[1] if rect_comp[1] > rect[1] else rect_comp[1]/rect[1]
			if (curr_match_y * curr_match_x) > match[0]:
				match = [curr_match_y * curr_match_x, rect_comp]
		#print(match[0])
		if match[0] > min_number_of_matches_ratio:
			#rects_a.remove(rect)
			rects_b.remove(match[1])
			matches += 1
			union += 1
		else:
			union += 1

	union += len(rects_b)

	print(matches/union)
	return matches/union
	
def categorise_rects( files , correlation=0.5, directory=".\\", save_file = "", load_file = ""):

	rectangles = {}
	categorised_rectangles = {}
	template_rectangles = {}
	if not load_file:
		for f in files:
			image = cv2.imread(directory + f);

			image = remove_lines(image)

			if image is not None:
				gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
				ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)

				invert = cv2.bitwise_not(thresh)
				bounds = bound(invert, 10, 20)
				stand = standardise_rectangles(bounds)
				rectangles[f] = stand
	else:
		rectangles = np.load(directory + load_file)

	if save_file:
		np.save(directory + save_file, rectangles)

	for file, curr_rect in rectangles.items():
		max_corr = ["",0]

		for category, template in template_rectangles.items():
			match = match_rects_jaccard(rect_list_a, template)
			if match > max_corr[1]:
				max_corr = [category,match]

		if max_corr[1] > correlation:
			categorised_rectangles[max_corr[0]].append(file)
		else:
			categorised_rectangles[file] = [file]
			template_rectangles[file] = curr_rect

	return categorised_rectangles


				#cv2.imshow(file, cv2.imread(dir_path+file))
				#cv2.imshow(file2, cv2.imread(dir_path+file2))
				#print(match_rects_jaccard(rect_list_a, rect_list_b))
				#cv2.waitKey(0)
				#cv2.destroyAllWindows()
	#cv2.waitKey(0)