import masker

import os
import cv2 
import sys

FPS = 30


def show_progress(current, total, label=''):
	percent_done = round(float(current)/total, 2)
	if label:
		label += ' '

	equals = '='*int(percent_done*30)
	arrow = '>'*(1-int(percent_done))
	dash = '-'*(29-int(percent_done*30))
	progress_bar = '[{0}{1}{2}]'.format(equals, arrow, dash, )

	status = '\r{0}{1} {2} of {3} generated ({4}%)'.format(label, progress_bar, current, total, round(percent_done*100, 1))
	sys.stdout.write(status)
	sys.stdout.flush()


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
