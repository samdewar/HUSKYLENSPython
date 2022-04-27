import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
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
		 
#
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

#format data into array
def format_data(unformatted_message):
	counter = 0
	formatted_message = []
	unformatted_message = unformatted_message.split('[')
	
	#skip first two blank lines
	for field in unformatted_message:
		if counter != 2:
			counter = counter + 1
			continue
		
		#remove extras
		field = field.replace("],","")
		field = field.replace("]","")
		field = field.replace("\'","")

		#add tp array
		formatted_message.append(field.split(","))
		
	return formatted_message

#count birds and add to dictionary
def count_birds(formatted_message):
	count_dict = {}

	for field in formatted_message:
		if field[1] not in  count_dict:
			count_dict[field[1]] = 1
		else:
			tmp = count_dict[field[1]] 
			tmp = tmp + 1
			count_dict[field[1]] = tmp
		
	return count_dict

#graph counted birds
def graph(counted_birds):
	names = list(counted_birds.keys())
	values = list(counted_birds.values())

	plt.bar(range(len(counted_birds)), values, tick_label=names)
	plt.show()
	
#main fucntion
def main(broker):
	connect_and_subscribe(broker)
	formatted_message = format_data(message)
	counted_birds = count_birds(formatted_message)
	graph(counted_birds)

main(broker_domain)
