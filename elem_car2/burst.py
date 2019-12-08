#import libraries of python opencv
import cv2
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import sys,os
import time
import picamera
import io

n = 5
park = [0,0,0]
size = len(park)

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
    time_out=start+20
    try:
        
        while(time.time()<time_out):
            camera.capture_sequence(filenames(), use_video_port=True)
            time.sleep(1)
            count = -1
            
            #iterating over n images
            while(count<n-1):
                count+=1
                #open image
                img = cv2.imread("/home/pi/Desktop/elem_car/photos/image%02d.jpg" % count)
                #print("on image: ",count,'\n')
                h0, w0 = img.shape[0:2]
                print(img.shape[0:2])

                # percent of original size
                #scale_percent = 10 
                #w1 = int(img.shape[1] * scale_percent / 100)
                #h1 = int(img.shape[0] * scale_percent / 100)
                #dim = (w1,h1)
                #resized = cv2.resize(img,dim)
                #print(resized.shape[0:2])

                subimg1 = img[120:h0-90, 0:int(w0/3)]
                subimg2 = img[130:h0-90, int(w0/3):int(2*w0/3)-20]
                subimg3 = img[130:h0-90, int(2*w0/3):w0-15]

                #use trained cars XML classifiers
                car_cascade = cv2.CascadeClassifier('cascade.xml')

                #convert video into gray scale of each frames
                gray1 = cv2.cvtColor(subimg1, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(subimg2, cv2.COLOR_BGR2GRAY)
                gray3 = cv2.cvtColor(subimg3, cv2.COLOR_BGR2GRAY)

                #detect cars in the video
                cars1 = car_cascade.detectMultiScale(gray1, scaleFactor = 1.1, minNeighbors =3,minSize = (100,100))
                cars2 = car_cascade.detectMultiScale(gray2, scaleFactor = 1.1, minNeighbors =3,minSize = (100,100))
                cars3 = car_cascade.detectMultiScale(gray3, scaleFactor = 1.1, minNeighbors =3,minSize = (100,100))

                #to draw a rectangle on each car
                i = 0
                cars = [cars1, cars2, cars3]
                subimg = [subimg1, subimg2, subimg3]
                
                while(i<size):
                    flag = False
                    for (x,y,w,h) in cars[i]:
                        #print(x,y,w,h)
                        park[i]=1
                        flag = True
                        cv2.rectangle(subimg[i],(x,y),(x+w,y+h),(0,255,0),2)
                    if(not(flag)):
                        park[i]=0
                    i = i+1

                #resize image
                #cv2.namedWindow("subimg1", cv2.WINDOW_NORMAL) 
                #cv2.namedWindow("subimg2", cv2.WINDOW_NORMAL) 
                #cv2.namedWindow("subimg3", cv2.WINDOW_NORMAL) 

                case=0
                for u in park:
                    if u==1:
                        case+=1
                        
                print("No. of cars present in total:",case)

                #display image
                #cv2.imshow('subimg1', subimg1)
                #cv2.imshow('subimg2', subimg2)
                #cv2.imshow('subimg3', subimg3)
                #cv2.waitKey(0)

                k=0
                while(k<size):
                    if(park[k]):
                        print("parking ",k+1," Occupied.")
                    else:
                        print("parking ",k+1," Unoccupied.")	

                    k=k+1 

                #fig=plt.figure('subimg1')
                #plt.imshow(subimg1)
                #plt.axis('off')
                #plt.show()
        

        #delete the images
        imgs = os.listdir('/home/pi/Desktop/elem_car/photos')
        for img in imgs:
            os.remove('/home/pi/Desktop/elem_car/photos/'+img)

        finish = time.time()
        #print('Captured %d frames at %.2ffps' % (
        #n,
        #n / (finish - start)))

    except KeyboardInterrupt:
        pass
        sys.exit()  
