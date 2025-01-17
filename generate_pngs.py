import os
import cv2 
import sys

import masker
from utils import show_progress

FPS = 30


def extract_from_video(video_path, output_dir, start_time=5, end_time=52, frame_increment=1):	
	start_frame = FPS * start_time
	end_frame = FPS * end_time
	frame = 0
	frames_processed = 0
	total_frames_to_process = int((end_frame - start_frame) / frame_increment)
	filename_char_length = len('%d.png' % total_frames_to_process)

	cap = cv2.VideoCapture(video_path)
	obj_extractor = masker.ObjectExtractor(extract_type='simple')

	ret = True
	while ret and (frame <= end_frame):
		ret, img = cap.read()

		if frame <= start_frame:
			# Learn background pixels using background subtraction
			obj_extractor.learnBackground(img)
		else:
			# Extract object and crop
			obj = obj_extractor.extractObject(img, thresh=100)
			obj_framed = masker.cropBox(obj)

			# Save image
			filename = os.path.join(output_dir, ('%d.png'%frames_processed).zfill(filename_char_length))
			cv2.imwrite(filename, obj_framed)

			# Print progress
			frames_processed += 1
			show_progress(frames_processed, total_frames_to_process)

		frame += frame_increment

	cap.release()
	cv2.destroyAllWindows()
	print('')
