"""
  # Simple WebCam capture
  # can zoom in and rotate image
  # and save a snapshot of image to a png file

  # Developed using Python 3.8 (Anaconda), on Windows 10
  #dependencies: 
  # pip install opencv-python
  # not sure if opencv-python also includes numpy as dependency... 
  # ! do not use conda install opencv (does not work properly)
  
# use the following keystrokes for :
#- r - rotate 90 degrees (done)
#- m - mirror image (done)
#- left mouse button to select Zoom region (ZoomBox) 
#   -->this only works if image is NOT mirrored or rotated
#- right mouse button to exit Zoom
#- c - save image as displayed on screen

#- next steps: 
#- do the math so that ZoomBox can be selected even when image is rotated/mirrored
#- change brightness/gain/contrast   
"""


from datetime import datetime
import cv2
import numpy as np
import sys
import time


def MouseEvents(event, x, y, flags, param):
  '''
  Callback function for mouse events-on-opencv
  
  this function is triggered whenever the mouse does anything
  
  specifically, for left mouse button clicks and right mouse button clicks
  
  output of function is pass-by-reference (params is a dictionary):
  params = {'x': int, 'y': int, 'flag': int}
  - x,y are the (x,y) positions of cursor when event happened
  - flag tells us which mouse button was depressed/released 
  
  See also:
    #https://stackoverflow.com/questions/50403176/mouse-events-on-opencv
    https://stackoverflow.com/questions/54605443/opencv-mouse-event-always-receive-event-10-and-flag-0-on-mouse-scroll
    
    event - gives the numerical value for the event
    (x,y) - position of cursor
    flags - additional information (e.g., scroll wheel up/down?)
    param - pass-by-reference variable for outputting data (use a dict for future extensibility)
  '''
  
  #event is an integer; here are the values it takes when a specific action by mouse has happened:
  #10 - scroll wheel move up/down (flag will tell us which direction)
  #1  - left mouse button down
  #2  - right mouse button down
  #3  - scroll wheel click down
  #4  - left button up
  #6  - scroll wheel click up
  #5  -  ??
  #7  - left mouse button double click
  #9  - scroll button double click
  #10 - scroll wheel move up/down (use flag to find up/down direction)  
  #11 - ??
  #12 - ??
  #13 - ??
  #14 - ??
  
  #used here:
  #1  - left mouse button down
  #4  - left button up 
  #2  - right mouse button down  
  
  if event in [ 1,4,2]:  # left button down/up, right mouse button down  
    param['x'] = x
    param['y'] = y
    param['flag'] = event
    param['TimeStamp'] = time.time()
    print('(x,y,flag) = (%2.2f,%2.2f,%i)\n'%(x,y,param['flag']))
  
  #use right mouse button to exit zoom mode
  #and left mouse button to enter zoom mode



def show_webcam(CamNum: int = 1, WindowName: str = 'Window1'):
  '''
  Heavily modified version of this:
  https://gist.github.com/tedmiston/6060034
  
  captures webcam image, then manipulates it (rotate, mirror, zoom) and displays it
  
  resolution hard-coded at 640x480
  
  '''
  
  cam = cv2.VideoCapture(CamNum, cv2.CAP_DSHOW) # create the capture object
  
  mirror: bool = False  # is image mirrored (flipped about x=0)?
  rotation: int = 0     #in degrees
  
  ZoomedIn: bool = False  
  
  # we will pass this dict into the mouse callback function
  # this obviates a global variable to store values
  params = {'x': 0, 'y':0, 'flag': 0, 'TimeStamp':0 }
  
  
  LastTimeStamp: float = 0.0 # last time that we updated due to mouse event
  cv2.setMouseCallback(WindowName, MouseEvents, params)
  
  ZoomBox = {'x0': [0,0], 'x1': [480, 640]}
  ZoomBoxNew = ZoomBox.copy()
    

  while True:
    ret_val, img = cam.read()

    #order of operation:
    # zoom first
    #rotate, then mirror flip, then zoom

    #only update zoom factor when not rotated or mirrored  

    
    if (ZoomedIn):
      # calculate the zoom box used 
      # ZoomBox = where on the image we will zoom in
      ZoomBoxNew['x0'][0] = min( ZoomBox['x0'][0] , ZoomBox['x1'][0] )
      ZoomBoxNew['x0'][1] = min( ZoomBox['x0'][1] , ZoomBox['x1'][1] )
      ZoomBoxNew['x1'][0] = max( ZoomBox['x0'][0] , ZoomBox['x1'][0] )
      ZoomBoxNew['x1'][1] = max( ZoomBox['x0'][1] , ZoomBox['x1'][1] ) 
      ZoomBox = ZoomBoxNew.copy()
      #print('About to Display New Zoom:' + str(ZoomBox))
      try:
        img = cv2.resize(img[ ZoomBox['x0'][1]:ZoomBox['x1'][1], 
        ZoomBox['x0'][0]:ZoomBox['x1'][0]], 
        dsize = [640, 480], 
        interpolation = cv2.INTER_AREA)
      except:
        print('Selected zoom region incorrectly')


    #how do we zoom rotate image?  
    if rotation == 270:
      img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if rotation == 180:
      img = cv2.rotate(img, cv2.ROTATE_180)
    if rotation == 90:
      img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    if mirror:      
      img = cv2.flip(img,1)    
  
    cv2.imshow(WindowName, img)  # finally, display the image


    # how do we deal with keyboard input?
    KeyPressed = cv2.waitKey(1) & 0xff

    if KeyPressed == 27: # Escape key
      print('exiting')
      break
    if KeyPressed == ord('m'): ## 'm' - mirror
      mirror = not(mirror)
      time.sleep(0.1)
    if KeyPressed == ord('r'):
      rotation  = (rotation+90)%360
    if KeyPressed == ord('c'): # take a screenCap
      datestr = datetime.now().strftime('%Y_%m_%d__%H_%M_%S_hrs')
      cv2.imwrite('Cam%i_%s_%s.png'%(CamNum, WindowName, datestr), img)

    # deal with mouse input here, which sets the ZoomBox
    # 
    if (rotation == 0) and (ZoomedIn == 0) and (mirror == False):
      if (LastTimeStamp<params['TimeStamp']): # some mouse event has happened
        LastTimeStamp = params['TimeStamp']  
        if params['flag'] in [1,4]:  # left button down or up
          ZoomBox['x0' if params['flag']== 1 else 'x1'] = [ params['x'], params['y'] ]
          if params['flag'] == 4:
            ZoomedIn = True
            print('After setting ZoomBox: '+str(ZoomBox))
    else: # Right mouse click resets entire image
      if (LastTimeStamp<params['TimeStamp']):
        LastTimeStamp = params['TimeStamp']  
        if params['flag'] in [2]:
          ZoomBox['x1'] = [  480 , 640 ]
          ZoomBox['x0'] = [    0 , 0   ]
          ZoomedIn = False
          rotation = 0
          mirror = False

  #finished capturing
  #let's free up some resources 
  cam.release()
  cv2.destroyAllWindows()





if __name__ == '__main__':
  # take as commandline input: CamNum, camera_display_name, 
  print(sys.argv)
  for i, arg in enumerate(sys.argv):
      print(f"Argument {i:>6}: {arg}")
  CamNum = int(sys.argv[1])
  WindowName = sys.argv[2]  # camera display name
  cv2.namedWindow(WindowName)
  show_webcam(CamNum = CamNum, WindowName = WindowName)
    
    
