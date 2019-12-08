# DISA-2019-final-files

## Arduino Mega Files:
  arduinoSketchFinal.ino - contains code run in the arduino mega during operation.

## Client RPi files:
  mqtt_pub_final.py - code written in python 3 for the client raspberry pi reading serial data from arduino mega and sending it
                        to the server raspberry pi using mqtt protocol.

## Server RPi files:
  mqtt_sub_final.py - code written in python 3 for the server raspberry pi reading data sent by the client and validates it using
                      car detection code.

## Car-detection system(elem_car2):
  
