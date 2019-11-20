# Data Tools for Mask R-CNN Artificial Training
This repo provides functions and scripts for generating artifical composites with pixelwise annotations for a given object, using videos taken of the object rotating atop a turntable. 

**WARNING** 
The functions and scripts in this repo are useful for prototyping but will result in data that is highly correlated. This should not be the method used to generate training data for a final model.

# Dependencies
- OpenCV
- SciPy
- Pandas
- NumPy
- Tensorflow<2.0.0
- PIL

## Installation
You can easily create an Anaconda environment using `environment.yml`

```bash
conda env create -f environment.yml
```

This should come with all of the dependencies listed above.

# Object Extraction Pipeline
## Step 1: Recording videos
The first step is to record videos of the object rotating on a turntable. We found that using a turntable that is lighter for a darker object, or darker for a lighter object, will help in the extraction process. Basically, having high contrast between the object and the background will help improve extraction results.

### Materials
- A good camera that won't dynamically adjust to changing colors during recording (disable auto exposure). As far as I know, this is not possible on an iPhone camera, and possibly with other smartphones as well.
- A tripod
- An electric turntable
- A stopwatch

### Steps
**NOTE**
*You can take multiple videos of an object* in order to capture perspectives from different camera elevations, or different object orientations (i.e. to capture an object's underside).

1. Set up the camera/tripod/turntable so that when the object is placed on top, it is entirely visible in the frame, and its *shadow is casted away from/not visible to the camera.*
2. Take the object **off** the turntable. Start recording, and only **after recording starts**, place the object on the turntable. You have **5 seconds** to place the object on the turntable with your hand. 
3. Start the stopwatch after placing the object. Stop recording after 1 minute. Currently, the script only processes the first 57 seconds after the video starts. This is just enough time for an entire rotation (at least for my turntable). It's OK if your video is longer than 57 seconds, but it should not be shorter.

## Step 2: Extract Object from Video and Generate Images
1. Place all videos in `data/videos`
2. Run `python scripts/generate_pngs_auto.py`
3. Do this for every object
4. Once you are happy with your results, rename each of the resulting folders in this format: `<class_id>-<class_name>`. If you have multiple videos of a particular class, then rename that folder to `<class_id>-<viewpoint_id>-<class_name>`. Class IDs must start at 0 and end at N-1, where N is the total number classes; in other words, start from 0 and don't skip numbers. 

## Step 3: Background scenery photos
It is a good idea to add several scenery photos to the `data/bg` directory. There is a python script (`resize_all_images.py`) in there that will resize them to an appropriate size once you have finished putting all your images in there. They must end in either `.JPG` or `.jpg`.

## Step 4: Generating the composites and their annotations
Run 

```bash
python scripts/generate_composites_multithread.py --composites <COMPOSITES> \
												  --threads <THREADS> \
												  --dataset <DATASET> \
												  --path <PATH>
```

Where 
- <COMPOSITES> is the total number of training images to generate
- <THREADS> is the number of threads/processes to use to generate the images
- <DATASET> is the name of the dataset
- <PATH> is the path to the directory containing the PNG folders.
