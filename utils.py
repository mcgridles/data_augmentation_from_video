import sys
import cv2
import numpy as np
from scipy.signal import convolve2d


def show_progress(current, total, label=''):
	percent_done = round(float(current)/total, 2)
	if label:
		label += ' '

	equals = '='*int(percent_done*30)
	arrow = '>'*(1-int(percent_done))
	dash = '-'*(29-int(percent_done*30))
	progress_bar = '[{0}{1}{2}]'.format(equals, arrow, dash)

	sys.stdout.write('\r{0}{1} {2}%'.format(label, progress_bar, percent_done*100))
	sys.stdout.flush()


def optical_flow(im1, im2):
	h, w, _ = im1.shape
	scale_factor = 50
	height = h * scale_factor / 100
	width = w * scale_factor / 100
	dim = (width, height)

	im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
	im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
	im1 = cv2.resize(im1, dim)
	im2 = cv2.resize(im2, dim)

	im1 = cv2.GaussianBlur(im1, (9, 9), 1)
	im2 = cv2.GaussianBlur(im2, (9, 9), 1)

	I_x = cv2.Sobel(im2, cv2.CV_64F, 1, 0, ksize=3);  # x gradient
	I_y = cv2.Sobel(im2, cv2.CV_64F, 0, 1, ksize=3);  # y gradient
	I_t = im2 - im1									  # time gradient

	I_xx = np.square(I_x)
	I_yy = np.square(I_y)
	I_xy = np.multiply(I_x, I_y)
	I_xt = np.multiply(I_x, I_t)
	I_yt = np.multiply(I_y, I_t)

	kernel = np.ones((9, 9))
	sum_Ixx = convolve2d(I_xx, kernel, mode='same', boundary='fill', fillvalue=0)
	sum_Iyy = convolve2d(I_yy, kernel, mode='same', boundary='fill', fillvalue=0)
	sum_Ixy = convolve2d(I_xy, kernel, mode='same', boundary='fill', fillvalue=0)
	sum_Ixt = convolve2d(I_xt, kernel, mode='same', boundary='fill', fillvalue=0)
	sum_Iyt = convolve2d(I_yt, kernel, mode='same', boundary='fill', fillvalue=0)

	u = np.zeros_like(im1)
	v = np.zeros_like(im1)
	for i in range(im1.shape[0]):
		for j in range(im1.shape[1]):
			A_2 = [
				[sum_Ixx[i,j], sum_Ixy[i,j]],
				[sum_Ixy[i,j], sum_Iyy[i,j]]
			]
			Ab = [
				[sum_Ixt[i,j]],
				[sum_Iyt[i,j]]
			]

			if np.linalg.det(A_2) == 0:
				u[i,j] = 0
				v[i,j] = 0
			else:
				of = -np.linalg.solve(A_2, Ab)
				u[i,j] = of[0]
				v[i,j] = of[1]

	return u, v
