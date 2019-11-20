import glob
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from generate_pngs import extract_from_video

VIDEO_DIR = os.path.join(ROOT_DIR, 'data/videos')


def generate_pngs(video_name, video_file):
	os.mkdir(video_name)
	basename = os.path.basename(video_file)
	print 'Found unprocessed video: ', basename
	print 'Generating pngs...'
		
	# Make the output folder
	extract_from_video(
		video_path=video_file, 
		output_dir=video_name, 
		start_time=5, 
		end_time=52, 
		frame_increment=3
	)


def main():
	video_files = glob.glob(os.path.join(VIDEO_DIR, '*.mov'))
	for video_file in video_files:
		video_name, _ = os.path.splitext(video_file)
		
		# If a directory with the file name of the video does not exist in the same folder,
		if not os.path.isdir(video_name):
			generate_pngs(video_name, video_file)


if __name__ == '__main__':
	main()
