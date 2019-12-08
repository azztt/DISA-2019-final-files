import paho.mqtt.client as mqtt
import pickle
import time
import os.path
import json

def calc_dur(in_time, out_time):
    t1 = in_time.split(':')
    t2 = out_time.split(':')

    secdiff = 0
    mindiff = 0
    hrdiff = 0

    if int(t2[2]) < int(t1[2]):
        secdiff = 60 - int(t1[2]) + int(t2[2])

        if int(t2[1]) < int(t1[1]):
            mindiff = 59 - int(t1[1]) + int(t2[1])

            if int(t2[0]) < int(t1[0]):
                hrdiff = 23 - int(t1[0]) + int(t2[0])

            else:
                hrdiff = int(t2[0]) - int(t1[0]) - 1
        else:
            mindiff = int(t2[1]) - int(t1[1]) - 1
            hrdiff = int(t2[0]) - int(t1[0])
    else:
        secdiff = int(t2[2]) - int(t1[2])
        if int(t2[1]) < int(t1[1]):
            mindiff = 59 - int(t1[1]) + int(t2[1])

            if int(t2[0]) < int(t1[0]):
                hrdiff = 23 - int(t1[0]) + int(t2[0])

            else:
                hrdiff = int(t2[0]) - int(t1[0]) - 1
        else:
            mindiff = int(t2[1]) - int(t1[1])
            hrdiff = int(t2[0]) - int(t1[0])

    dur = str(hrdiff) + ":" + str(mindiff) + ":" + str(secdiff)

    return dur

def init_dict(park):
    with open('./bin_log.txt', 'rb') as file:
        park = pickle.load(file)
    
    return park

def write_dict(park):
    with open('./bin_log.txt', 'wb') as file:
        pickle.dump(park, file)

def log(mess):
    cur_time = time.asctime()
    ar = cur_time.split()
    cur_time = ar[3] + ' ' +  ar[1] + ' ' +  ar[2] + ', ' + ar[4]
    with open('./logfile.txt', 'a') as file:
        file.write('At ' + cur_time + ': ' + mess + '\n')

def Park_Occ(park, pNo):
    cur_time = time.asctime()
    ar = cur_time.split()
    cur_time = ar[3] + ' ' +  ar[1] + ' ' +  ar[2] + ', ' + ar[4]

    if park["pStatus"][pNo] == False:
        park["pStatus"][pNo] = True
        park["occ_time"][pNo].append(cur_time)

    return park
    
def Park_Left(park, pNo):
    cur_time = time.asctime()
    in_time = park["occ_time"][pNo][len(park["occ_time"][pNo]) - 1]
    in_time = in_time.split()[0]
    ar = cur_time.split()
    cur_time = ar[3] + ' ' +  ar[1] + ' ' +  ar[2] + ', ' + ar[4]
    out_time = cur_time.split()[0]

    if park["pStatus"][pNo] == True:
        park["pStatus"][pNo] = False
        park["left_time"][pNo].append(cur_time)
        park["occ_duration"][pNo].append(calc_dur(in_time, out_time))

    return park
         
 
MQTT_SERVER = "localhost"
MQTT_PATH = "park_info"
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # if first time operation, initialising log file 
    if os.path.isfile('./bin_log.txt') == False:
        park1 = {"pStatus": {1: False, 2: False}, "occ_time": {1: [], 2: []}, "left_time": {1: [], 2: []}, "occ_duration": {1: [], 2: []}}
        with open('./bin_log.txt', 'wb') as file:
            pickle.dump(park1,file)
        
        mess = "Smart Parking System started"
        log(mess)
        del mess

    messg = str(msg.payload.decode('utf-8'))
    messg = messg.rstrip()
    keys = messg.split()
    pNo = int(keys[1])
    state = keys[2]

    preStatus_json = {}
    preStatus = False

    if os.path.isfile('./log.json'):
        with open('./log.json','r') as json_file:
            preStatus_json = json.load(json_file)
        
        preStatus = preStatus_json["pStatus"][str(pNo)]
    
    if state == 'occupied':
        log('Received from pi: ' + messg)

        if os.path.isfile('./log.json') == False:
            preStatus = False

        if preStatus != True:
            reqLine = " sdg"
            with open('./tempStatus.txt', 'r') as file:
                current_line = 1
                for line in file:
                    if current_line == pNo:
                        reqLine = line
                        break
                    current_line += 1
            
            if reqLine.split()[2] == "Occupied":
                log('Confirmed by camera: True')
                park1 = {"pStatus": {1: False, 2: False}, "occ_time": {1: [], 2: []}, "left_time": {1: [], 2: []}, "occ_duration": {1: [], 2: []}}
                park1 = init_dict(park1)

                park1 = Park_Occ(park1, pNo)

                write_dict(park1)
                with open('./log.json', 'w') as json_file:
                    json.dump(park1, json_file)        

                del park1
            else:
                log('Confirmed by camera: False')
        else:
            log('Redundant data... ignoring')

    elif state == 'left':
        log('Received from pi: ' + messg)

        if os.path.isfile('./log.json') == False:
            preStatus = True

        if preStatus != False:
            reqLine = "sdg"
            with open('./tempStatus.txt', 'r') as file:
                current_line = 1
                for line in file:
                    if current_line == pNo:
                        reqLine = line
                        break
                    current_line += 1

            if reqLine.split()[2] == "Unoccupied":
                log('Confirmed by camera: True')
                park1 = {"pStatus": {1: False, 2: False}, "occ_time": {1: [], 2: []}, "left_time": {1: [], 2: []}, "occ_duration": {1: [], 2: []}}
                park1 = init_dict(park1)

                park1 = Park_Left(park1, pNo)

                write_dict(park1)
                with open('./log.json', 'w') as json_file:
                    json.dump(park1, json_file)

                del park1
            else:
                log('Confirmed by camera: False')
        else:
            log('Redundant data... ignoring')
        
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()