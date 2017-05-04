#file handling imports
import sys
import os
from os import listdir
from os.path import isfile, join
#opencv imports
import cv2
import numpy as np
import copy

import pickle
from matplotlib import pyplot as plt


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



def show_sum( sum_img, window_name):
	sum_mat = copy.deepcopy(sum_img)
	print(sum_mat)
	maxval = sum_mat[-1][-1]
	for y in range(0,len(sum_mat)):
		for x in range(0,len(sum_mat[0])):
			sum_mat[y][x] = int((float(sum_mat[y][x]) / float(maxval)) * 255)
	print(sum_mat)
	cv2.imshow(window_name,sum_mat.astype(np.ubyte))
	cv2.waitKey(0)
	#cv2.destroyAllWindows()


def sum_rect( rect, sum_img):
	#print(rect)
	#print(sum_img)
	x1,y1,x2,y2 = rect
	if x2 >= len(sum_img): x2 = len(sum_img)-1
	if y2 >= len(sum_img[0]): y2 = len(sum_img[0])-1
	return sum_img[x2][y2] + sum_img[x1-1][y1-1] - sum_img[x1-1][y2] - sum_img[x2][y1-1]

def sum_expand(rect, sum_img, border=10):
	x1,y1,x2,y2 = rect
	#print(sum_rect([x1,y1,x2+border,y2], sum_img))
	#print(sum_rect([x1,y1,x2,y2], sum_img))
	if sum_rect([x1,y1,x2+border,y2], sum_img) > sum_rect([x1,y1,x2,y2], sum_img):
		return [x1,y1,x2+border,y2]

	if sum_rect([x1,y1,x2,y2+border], sum_img) > sum_rect([x1,y1,x2,y2], sum_img):
		return [x1,y1,x2,y2+border]

	return rect



#sum bound
def sum_bound( img, border=3, min_size=50):

	sum_img = sum_areas(img)
	show_sum(sum_img, "sum")

	for x in range(1,len(sum_img)):
		for y in range(1,len(sum_img[0])):
			if img[x][y] and not in_rects((x,y),rectangles):
				print("new rectangle at ", x, " ", y)
				
				rect = [x,y,x,y]
				while True:
					#print(rect)
					expanded_rect = sum_expand(rect, sum_img)
					#print("exp rectangle at ", expanded_rect)
					cv2.waitKey(0)
					if expanded_rect == rect: break
					rect = expanded_rect

				x1,y1,x2,y2 = expanded_rect

				if (x2-x1 > min_size) and (y2-y1 > min_size):
					rectangles.append(expanded_rect)
					print(expanded_rect)

	return rectangles








# return rectangles surrounding foreground areas on document : requires foreground True, background False
def bound( img , border=3, min_size=5):

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
