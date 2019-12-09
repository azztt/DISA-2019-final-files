import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

#MQTT_SERVER = "10.194.9.75"
# My laptop:
#MQTT_SERVER = "10.194.10.180"
MQTT_SERVER = "10.194.1.70"
# Head Pi:
#MQTT_SERVER = "10.194.19.86"
MQTT_PATH = "park_info"
client = mqtt.Client()
client.connect(MQTT_SERVER, 1883, 60)
print("Connected to server Raspberry Pi")

#mess = str(ser.readline())

#publish.single(MQTT_PATH, mess, hostname=MQTT_SERVER)

#client.loop_forever()

while True:
    mess = ser.readline()
    #publish.single(MQTT_PATH, mess, hostname=MQTT_SERVER)
    client.publish(MQTT_PATH, mess)
    print("Sent: " + str(mess))
