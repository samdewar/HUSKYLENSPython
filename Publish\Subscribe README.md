# MQTT python

Python files for publishing and subscribing to a Mosquitto MQTT broker  

Variables may be named bird related items as that was the project it was initally for

# Installation
Packages Time, Paho and CSV must be installed to use this code

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 

```bash
pip install paho-mqtt
```

CSV and time are pre-installed packages however if not installed follow instructions bellow including  

```bash
pip install python-csv
```
```bash
pip install paho-mqtt
```
# Usage of Publish
Call function main()

```python
status = main(filename, broker)
```
filename is the name of the CSV file you wish to read data from  
broker is the MQTT broker IP or domain name  
status is a string variable that either returns confirmation or error message for usage  

# Publish Process

First it will read from the file and check if there is data to be published
```python
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
```


```python
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
```

It will then attempt to connect to the broker and publish the data as a string. If unsuccessful in connection it will exit and return an error status. This is so the overall
script can be called over and over allowing for multiple attempts.

```python
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
```

```python       
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
```

# Subscribe Process
The subscription process is similar however data is recieved instead of sent. This data is then decoded like a packet and the payload is extracted.

```python
#decode message
def on_message(client, userdata, msg):
        global message
        message = msg.payload
        client.disconnect()
        print(message)
```

The payload is then formatted back into an array from a string.

```python
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
```
The instances are then counted and plotted into a bar chart

```python
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
```
```python
#graph counted birds
def graph(counted_birds):
	names = list(counted_birds.keys())
	values = list(counted_birds.values())

	plt.bar(range(len(counted_birds)), values, tick_label=names)
	plt.show()

```
# Contact
Any questions please contact me at: paul.crichton@outlook.com

Many Thanks,
Paul
