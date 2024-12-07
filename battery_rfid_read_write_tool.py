import RPi.GPIO as GPIO
import json
import os
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
    cont = True;
    while(cont):
        write = input("Read or Write? (R/W):").capitalize() == "W"
        if (write):
            id = int(input("What is the battery ID?"))
            year = int(input("In what year was the battery purchased?"))
            cap = float(input("What was the last tested capacity of the battery in Ah?"))
            type = "COMP" if input("Is this a competition battery? (Y/N):").capitalize() == "Y" else "TEST"
            mfg = input("Who manufactured the battery?")
            batteryData = [id,year,cap,type,mfg]
            dictStr = json.dumps(batteryData)
            print(dictStr)
            reader.write(dictStr)
            print("-------------------")
            print("Written")
            print("-------------------")
        else:
            try:
                id, text = reader.read()
                batteryData = json.loads(text)
                print("-------------------")
                print("Tag ID: " + str(id))
                print("Battery ID: "+ str(batteryData[0]))
                print("Purchase Year: " + str(batteryData[1]))
                print("Battery Capacity (Ah): " + str(batteryData[2]))
                print("Type: " + str(batteryData[3]))
                print("Manufacturer: " + str(batteryData[4]))
                print("-------------------")
            except json.decoder.JSONDecodeError:
                print("Failed to read card")
        cont = (input("Continue? (Y/N):").capitalize() == "Y")
            
finally:
        GPIO.cleanup()
