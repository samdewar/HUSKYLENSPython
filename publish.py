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
    

#For loggin and maintinence 
def on_log(client, userdata, level, buf):
    print("log: ",buf)
    
#Open CSV file and read data to array
def open_file(filename):
    try:
        file_CSV = open(filename)
        data_CSV = csv.reader(file_CSV)
        list_CSV = list(data_CSV)
        return list_CSV
    except Exception as e: #Return error
        print("Error with file: ", e)
        return list_CSV 


#check if there is a connection and publish data
def on_connect(client, userdata, flags, rc):
    if rc == 0: # 0 is correctly connected
        print("Connected")
        client.connected_flag=True
        try:
            print("Publishing Data")
            client.publish("birds/data", str_bird_array, qos=0, retain=True)
            time.sleep(7)
            print("Published")
        except Exception as e: #Return Error in publishing
            print("Error Publishing Data: ", e)        
        client.disconnect()
    else: #Return Status code
        print("Error connection: ", rc)
        client.disconnect()

        
        
#Create Client and run connection and publish scripts
def connect_and_publish(broker, bird_array):
        mqtt.Client.connected_flag=False
        
        #Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
        client = mqtt.Client("lions_gate") # Client
        
        client.loop_start() # Client loop
        
        #Callback for displaying log data
        client.on_log=on_log
        
        #start coonection attempt
        client.connect(broker, port=1883, keepalive=60)
        print("Attempting COnnection")
                
        client.on_connect=on_connect #callback function
        
        while client.connected_flag == False: #Wait for connection
            print("Waiting...")
            time.sleep(1)
        
        #Callback for displaying data only used in subscription scripts
        client.on_message=on_message
    
        
        client.loop_stop() # Loop stop

#main function - check if data then start connection script
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
	
#filename and broker domain    
filename = "birds.csv"
broker = "127.0.0.1"    
    
#main call and status of scripts 
status = main(filename, broker)
print(status)


