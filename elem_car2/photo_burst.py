#import libraries of python opencv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import sys
import time
from picamera import PiCamera

n = 5
picamera = Picamera()
def filenames():
    frame = 0
    while frame < n:
        yield '/home/pi/Desktop/elem_car/photos/image%02d.jpg' % frame
        frame += 1

with picamera.PiCamera(resolution='720p', framerate=30) as camera:
    camera.start_preview()
    # Give the camera some warm-up time
    time.sleep(2)
    start = time.time()
    time_out=time.time()+60*3
    while(time.time()<time_out):
          camera.capture_sequence(filenames(), use_video_port=True)
          k=0
          while(k<n):
              #open images
              img = cv2.imread("/home/pi/Desktop/elem_car/photos/image%02d.jpg" % k)
              old_height, old_width = img.shape[0:2]
              print(img.shape[0:2])
              subimg1=img[0:old_height,0:int(old_width/3)]
              subimg2=img[0:old_height,int(old_width/3):int(2*old_width/3)]
              subimg3=img[0:old_height,int(2*old_width/3):old_width]
              width=275
              height=183
              dim=(height,width)
              subimg1=cv2.resize(old1,dim)
              subimg2=cv2.resize(old2,dim)
              subimg3=cv2.resize(old3,dim)
                          
              try:
                  #use trained cars XML classifiers
                  car_cascade = cv2.CascadeClassifier('best_cars.xml')

                  #convert video into gray scale of each frames
                  gray1 = cv2.cvtColor(subimg1, cv2.COLOR_BGR2GRAY)
                  gray2 = cv2.cvtColor(subimg2, cv2.COLOR_BGR2GRAY)
                  gray3 = cv2.cvtColor(subimg3, cv2.COLOR_BGR2GRAY)
                  #detect cars in the video
                  cars1 = car_cascade.detectMultiScale(gray1, scaleFactor = 1.1, minNeighbors =2)#minSize = (103,103))
                  cars2 = car_cascade.detectMultiScale(gray2, scaleFactor = 1.1, minNeighbors =2)#minSize = (103,103))
                  cars3 = car_cascade.detectMultiScale(gray3, scaleFactor = 1.1, minNeighbors =2)#minSize = (103,103))


                  #to draw arectangle in each cars
                  i=0
                  park=[0,0,0]
                  size=len(park)
                  for (x,y,w,h) in cars1:
                      #print(x,y,w,h)
                      park[size-1-i]=1
                      i=i+1
                      cv2.rectangle(subimg1,(x,y),(x+w,y+h),(0,255,0),2)

                  for (x,y,w,h) in cars2:
                      #print(x,y,w,h)
                      park[size-1-i]=1
                      i=i+1
                      cv2.rectangle(subimg2,(x,y),(x+w,y+h),(0,255,0),2)      

                  for (x,y,w,h) in cars3:
                      #print(x,y,w,h)
                      park[size-1-i]=1
                      i=i+1
                      cv2.rectangle(subimg3,(x,y),(x+w,y+h),(0,255,0),2)      
                            

                  #resize image
                  #cv2.namedWindow("subimg1", cv2.WINDOW_NORMAL) 
                  #cv2.namedWindow("subimg2", cv2.WINDOW_NORMAL) 
                  #cv2.namedWindow("subimg3", cv2.WINDOW_NORMAL) 
                  print("No. of cars present in total:",i)
                  #display image
                  #cv2.imshow('subimg1', subimg1)
                  #cv2.imshow('subimg2', subimg2)
                  #cv2.imshow('subimg3', subimg3)
                  #cv2.waitKey(0)
                  k=0
                  while(k<size):
                      if(park[k]):
                          print("parking ",k+1," is occupied.")
                      k=k+1	

                  fig=plt.figure('img')
                  plt.imshow(img)
                  plt.axis('off')
                  plt.show()


              except KeyboardInterrupt:
                  pass
                  sys.exit()           
                          
    
          #delete the images
          imgs = os.listdir('/home/pi/Desktop/elem_car/photos')
          for img in imgs:
              os.remove('/home/pi/Desktop/elem_car/photos/'+img)
              
          finish = time.time()
          print('Captured %d frames at %.2ffps' % (
          n,
          n / (finish - start)))
    

    
