import sys
import os
import glob
import argparse
import multiprocessing as mp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate_composites import generate_composites

this_dir = os.path.dirname(os.path.abspath(__file__))

def print_progress(img_dir, total_composites, indices_tuples):
	num_pics = 0
	while num_pics != total_composites:
		if os.path.exists(img_dir):
			num_pics = len(glob.glob(img_dir+'/*.jpg'))
			sys.stdout.write('\r'+str(num_pics)+' of '+str(total_composites)+' generated')
			sys.stdout.flush()

def print_progress(img_dir, total_composites, indices_tuples):
	num_pics = 0
	while num_pics != total_composites:
		if os.path.exists(img_dir):
			all_composites = glob.glob(os.path.join(img_dir, '*.jpg'))
			num_pics = len(all_composites)
			progress = ''
			for i in indices_tuples:
				pics_per_generator = [j for j in all_composites if i[0] <= int(os.path.basename(j).split('.')[0]) <= i[1]]
				progress += '%d for %d-%d, ' % (len(pics_per_generator), i[0], i[1])
			sys.stdout.write('%d of %d generated: ' % (num_pics, total_composites) + progress[:-2] + '\r')
			sys.stdout.flush()


def main():
	parser = argparse.ArgumentParser(description='Process some integers.')

	parser.add_argument('--composites', '-c', type=int, metavar='N', help='Total number of composites to generate', default=1000)
	parser.add_argument('--threads', '-t', type=int, metavar='N', help='Number of threads (processes) for creating composites', default=1)
	parser.add_argument('--dataset', '-d', help='Name of the dataset')
	parser.add_argument('--path', '-p', help='Path to directory containing PNG folders')

	args = parser.parse_args()
	
	# Parse arguments
	total_composites = args.composites
	num_processes    = args.threads
	dataset          = args.dataset 
	png_dir          = args.path
	batch_size       = int(float(total_composites)/float(num_processes))

	# Figure out number of classes
	pngs_folders = [i for i in glob.glob(os.path.join(png_dir,'*')) if os.path.isdir(i)]
	num_classes = 0 
	for png_folder in pngs_folders:
		png_folder_id = int(os.path.basename(png_folder).split('-')[0])
		num_classes = max(num_classes, png_folder_id + 1)

	# Create directories
	ann_dir = os.path.join(this_dir, 'data/generated_pictures/annotations_' + dataset)
	img_dir = os.path.join(this_dir, 'data/generated_pictures/images_' + dataset)
	for directory in [ann_dir, img_dir]:
		if not os.path.exists(directory):
			os.makedirs(directory)

	# Spawn composite generator scripts
	processes = list()
	indices_tuples = list()
	for i in xrange(num_processes):
		start_index = i * batch_size
		end_index = min((i+1) * batch_size - 1, total_composites)

		p = mp.Process(target=generate_composites, args=(png_dir, start_index, end_index, dataset, False))
		p.start()
		processes.append(p)

		indices_tuples.append((start_index, end_index))

	# Spawn print progress process
	print_p = mp.Process(target=print_progress, args=(img_dir, total_composites, indices_tuples))
	print_p.start()

	for p in processes:
		p.join()

	print_p.join()


if __name__ == '__main__':
	main()
