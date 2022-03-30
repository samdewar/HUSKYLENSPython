import paho.mqtt.client as mqtt
import time

#variables
broker_domain="127.0.0.1"

#decode message
def on_message(client, userdata, msg):
        global message
        message = msg.payload
        client.disconnect()
        print(message)
    
#logging
def on_log(client, userdata, level, buf):
    print("log: ",buf)

#check if there is a connection
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)


#check if there is a connection
def on_connect(client, userdata, flags, rc):        
        client.subscribe("birds/data")
        time.sleep(10)
		 

def connect_and_subscribe(broker):
		global connection
		#Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
		client = mqtt.Client("lions_gate")
		#start coonection attempt
		client.connect(broker, port=1883, keepalive=60)
		connection = True
		
       
		client.loop_start()        
                
		client.on_connect=on_connect #callback function
		print("Connecting to ",broker)
       
		#Callback for displaying data
		client.on_message=on_message
    
		#Callback for displaying log data
		client.on_log=on_log
        
		client.loop_forever()


6
def main(broker):
	connect_and_subscribe(broker)
	
main(broker_domain)
