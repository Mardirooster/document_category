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

def is_in( rect, img ):
	return rect[0] < len(img[0]) and rect[1] < len(img) and rect[2] < len(img[0]) and rect[3] < len(img)

#def expand1( rect, sum_img, border):


def in_rect(point, rect):
	px,py = point
	rx1,ry1,rx2,ry2 = rect
	return px >= rx1 and px <= rx2 and py >= ry1 and py <= ry2  

def in_rects( point, rects):
	for rect in rects:
		if in_rect(point, rect):
			return True;
	return False


def sum_areas( img, border=3):

	sum_mat = np.full((len(img),len(img[0])), 0, dtype= int)

	for y, row in enumerate(img):
		for x, pixel in enumerate(row):
			if y:
				if pixel:
					sum_mat[y][x] = sum_mat[y-1][x] + 1
				else:
					sum_mat[y][x] = sum_mat[y-1][x]
			else:
				if pixel: sum_mat[y][x] = 1
		#print(sum_mat[y])

	for y, row in enumerate(sum_mat):
		for x, pixel in enumerate(row):
			if x:
				sum_mat[y][x] = sum_mat[y][x-1] + sum_mat[y][x]

	maxval = sum_mat[-1][-1]
	print(maxval)
	# for y, row in enumerate(sum_mat):
	# 	for x, pixel in enumerate(row):
	# 		sum_mat[y][x] = int((float(sum_mat[y][x]) / float(maxval)) * 255)

	return sum_mat

# return rectangles surrounding foreground areas on document : requires foreground True, background False
def bound( img , border=3):

	rectangles = []

	cur_rectangle = []
	#sum_img = sum_areas(img)

	for y, row in enumerate(img):
		for x, pixel in enumerate(row):
			if pixel and not in_rects((x,y),rectangles):
				cur_rectangle = [x,y,x,y]
				#print("found corner! ", x,y)
				while True:
					new_rect = expand( cur_rectangle, img, border)

					# new_rect = expand( cur_rectangle, img, border)
					if cur_rectangle == new_rect:
						break
					else:
						cur_rectangle = list(new_rect)

				x1,y1,x2,y2 = cur_rectangle

				if (x2-x1 > min_size) and (y2-y1 > min_size):
					rectangles.append(cur_rectangle)

	return rectangles


def standardise_rectangles( rectangles ):
	print(rectangles)
	simp_rect = []

	for rect in rectangles:
		simp_rect.append([rect[2] - rect[0], rect[3] - rect[1]])

	print(simp_rect)
	return sorted(simp_rect)
