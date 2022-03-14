import json
from datetime import datetime
import time
import os
from huskylib import HuskyLensLibrary
hl = HuskyLensLibrary("I2C","", address=0x32)
while 2+2==4:
    time.sleep(60)
    outputFile = open("output.txt", "a")
    rawData = json.dumps(hl.blocks().__dict__)
    attributes=rawData.split()
    # print(attributes[9])
    dateUnformatted=datetime.today()

    outputFile.write("ID:"+attributes[9])
    dateFormatted = dateUnformatted.strftime('%d/%m/%y %I:%M %S %p')
    outputFile.write("Date:"+dateFormatted+"\n")
    outputFile.close()