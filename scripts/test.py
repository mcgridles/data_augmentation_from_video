import os
import sys
import cv2

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from utils import optical_flow


if __name__ == '__main__':
	video_path = os.path.abspath(sys.argv[1])
	
	cap = cv2.VideoCapture(video_path)
	num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

	if cap.isOpened():
		cap.set(cv2.CAP_PROP_POS_FRAMES, num_frames / 2)

		_, frame1 = cap.read()
		_, frame2 = cap.read()

		u, v = optical_flow(frame1, frame2)

		cv2.imshow('U', u)
		k = cv2.waitKey() & 255
		if ord(k) == 'q':
			cv2.destroyAllWindows()

		cv2.imshow('V', v)
		k = cv2.waitKey() & 255
		if ord(k) == 'q':
			cv2.destroyAllWindows()

	cap.release()
	cv2.destroyAllWindows()
