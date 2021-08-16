  Simple WebCam capture
  can zoom in and rotate image
  and save a snapshot of image to a png file

  Developed using Python 3.8 (Anaconda), on Windows 10

  Dependencies: 
  pip install opencv-python
  not sure if opencv-python also includes numpy as dependency... 
  ! do not use     conda install opencv (does not work properly)
  
use the following keystrokes for :
- r - rotate 90 degrees (done)
- m - mirror image (done)
- left mouse button to select Zoom region (ZoomBox) 
  -->this only works if image is NOT mirrored or rotated
- right mouse button to exit Zoom
- c - save image as displayed on screen

TODO:
- do the math so that ZoomBox can be selected even when image is rotated/mirrored
- change brightness/gain/contrast of image