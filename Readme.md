  # Simple WebCam capture
  can zoom in and rotate image
  and save a snapshot of image to a png file

  Developed using Python 3.8 (Anaconda), on Windows 10

  ## Dependencies: 
opencv-python     4.5.3.56
numpy             1.21.1


## Instructions: 
use the following keystrokes for :
- r - rotate 90 degrees 
- m - mirror image  
- left mouse button to select Zoom region (ZoomBox) 
  -->this only works if image is NOT mirrored or rotated
- right mouse button to exit Zoom
- c - save image as displayed on screen

You can start multiple instances at the (Windows) terminal:
> start python SimpleCam_Final.py 1 cam1
> start python SimpleCam_Final.py 2 cam2

where 1,2 are the indices of the capture devices.

TODO:
- do the math so that ZoomBox can be selected even when image is rotated/mirrored
- change brightness/gain/contrast of image
