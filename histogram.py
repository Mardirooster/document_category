

def categorise_histograms( files ):
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