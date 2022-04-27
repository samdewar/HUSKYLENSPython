import paho.mqtt.client as mqtt
import time
import csv
import numpy

#decode message from subscription
def on_message(client, userdata, msg):
        global message
        message = msg.payload
        client.disconnect()
        print(message)
    

#logging
def on_log(client, userdata, level, buf):
    print("log: ",buf)
    

def open_file(filename):
    try:
        file_CSV = open(filename)
        data_CSV = csv.reader(file_CSV)
        list_CSV = list(data_CSV)
        return list_CSV
    except Exception as e:
        print("Error with file: ", e)
        return list_CSV 


#check if there is a connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        client.connected_flag=True
        try:
            print("Publishing Data")
            client.publish("birds/data", str_bird_array, qos=0, retain=True)
            time.sleep(7)
            print("Published")
        except Exception as e:
            print("Error Publishing Data: ", e)        
        client.disconnect()
    else:
        print("Error connection: ", rc)
        client.disconnect()

        
        

def connect_and_publish(broker, bird_array):
        mqtt.Client.connected_flag=False
        
        #Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
        client = mqtt.Client("lions_gate")
        
        client.loop_start()
        
        #Callback for displaying log data
        client.on_log=on_log
        
        #start coonection attempt
        client.connect(broker, port=1883, keepalive=60)
        print("Attempting COnnection")
                
        client.on_connect=on_connect #callback function
        
        while client.connected_flag == False:
            print("Waiting...")
            time.sleep(1)
        
        #Callback for displaying data
        client.on_message=on_message
    
        
        client.loop_stop()

def main(csv_filename, broker):
    #variables
    global str_bird_array
    
    bird_array = open_file(csv_filename)
    if not bird_array:
        status = "No Data"
        return status
    else:
        str_bird_array = str(bird_array) 
        connect_and_publish(broker, str(bird_array))
        status = "Data has been published"
        return status
	
    
filename = "birds.csv"
broker = "127.0.0.1"    
    
status = main(filename, broker)
print(status)


