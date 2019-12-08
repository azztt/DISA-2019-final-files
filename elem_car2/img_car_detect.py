#import libraries of python opencv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
#mpl.rcParams.update({'figure.max_open_warning': 0})
import sys
import time

#open image
img = cv2.imread("image.jpg")
height, width = img.shape[0:2]
#subimg1=img[0:height,70:1400]
#subimg2=img[0:height,1401:2680]
#subimg3=img[0:height,2681:4000]
#print(img.shape[0:2])

try:
    #use trained cars XML classifiers
    car_cascade = cv2.CascadeClassifier('best_cars.xml')

    #convert video into gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #detect cars in the video
    cars = car_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors =3,minSize = (590,550))

    #to draw arectangle in each cars
    i=0
    park=[0,0,0]
    size=len(park)
    for (x,y,w,h) in cars:
        #print(x,y,w,h)
        park[size-1-i]=1
        i=i+1
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)      

    #resize image
    #cv2.namedWindow("img", cv2.WINDOW_NORMAL) 
    print("No. of cars present in total:",i)
    #display image
    #cv2.imshow('img', img)
    #cv2.waitKey(0)
    k=0
    while(k<size):
        if(park[k]):
            print("parking ",k+1," is occupied.")
        else:
            print("parking",k+1,"is unoccupied.")
                        
        k=k+1   

    fig=plt.figure('img')
    plt.imshow(img)
    plt.axis('off')
    plt.show()

except KeyboardInterrupt:
    pass
    sys.exit() 
