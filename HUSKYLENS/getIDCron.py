#configuration info found at https://github.com/HuskyLens/HUSKYLENSPython/blob/master/Raspberry%20Pi%20Tutorial.md
#this version of getID does not contain a loop and so must be run every minute by cron (if that works)
import json
from datetime import datetime
import time
import os
from huskylib import HuskyLensLibrary
hl = HuskyLensLibrary("I2C","", address=0x32)
outputFile = open("birds.csv", "a")#opens the output file on append mode
rawData = json.dumps(hl.blocks().__dict__)#reads the id in view of camera
attributes=rawData.split()#split the string into an array based on spaces
# print(attributes[9])
dateUnformatted=datetime.today()#gets todays date

outputFile.write("ID:"+attributes[9])#write the id (9 in the array)
dateFormatted = dateUnformatted.strftime('%d/%m/%y %I:%M')#format date
outputFile.write("Date:"+dateFormatted+"\n")#write formatted date on same line as id
outputFile.close()#close file