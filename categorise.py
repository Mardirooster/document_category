#opencv imports
import cv2
import numpy as np
#file handling imports
import sys
import os

def categorise_histograms( files , correlation=0.09 , compare_method=cv2.HISTCMP_CORREL, directory=".\\"):

	template_histograms = {}
	categorised_hist = {}
	print(files)
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

	print(categorised_hist)
	return categorised_hist		



def match_rects( rects_a_param, rects_b_param , min_match=0.5):
	print("hi")
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
		print(match[0])
		if match[0] > min_match:
			rects_a.remove(rect)
			rects_b.remove(match[1])
			matches += 1

	print(rects_a)
	print(rects_b)
	print(matches)
	return matches


