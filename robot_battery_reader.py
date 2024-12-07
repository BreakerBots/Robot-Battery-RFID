import RPi.GPIO as GPIO
import json
import ntcore
import time
from mfrc522 import SimpleMFRC522

ntInst = ntcore.NetworkTableInstance.getDefault()
ntInst.startClient4("Battery Reader")
ntInst.setServerTeam(5104)
ntInst.startDSClient()
batteryDatatable = ntInst.getTable("Battery")
readBattPub = batteryDatatable.getBooleanTopic("has_tag").publish()
tagIDPub = batteryDatatable.getIntegerTopic("tag_id").publish()
battIDPub = batteryDatatable.getIntegerTopic("battery/id").publish()
yearPub = batteryDatatable.getIntegerTopic("battery/year").publish()
capPub = batteryDatatable.getDoubleTopic("battery/cap").publish()
typePub = batteryDatatable.getStringTopic("battery/type").publish()
mfgPub = batteryDatatable.getStringTopic("battery/mfg").publish()
try:
    reader = SimpleMFRC522()
    hasReadBattery = False
    while(True):
        readBattPub.setDefault(False)
        tagIDPub.setDefault(0)
        battIDPub.setDefault(0)
        yearPub.setDefault(0)
        capPub.setDefault(0.0)
        typePub.setDefault("NONE")
        mfgPub.setDefault("NONE")
        try:
            id, text = reader.read()
            batteryData = json.loads(text)
            print("SUCCESS!")
            print("-------------------")
            print("Tag ID: " + str(id))
            print("Battery ID: "+ str(batteryData[0]))
            print("Purchase Year: " + str(batteryData[1]))
            print("Battery Capacity (Ah): " + str(batteryData[2]))
            print("Type: " + str(batteryData[3]))
            print("Manufacturer: " + str(batteryData[4]))
            print("-------------------")
            hasReadBattery = True
            readBattPub.set(hasReadBattery)
            tagIDPub.set(id)
            battIDPub.set(batteryData[0])
            yearPub.set(batteryData[1])
            capPub.set(batteryData[2])
            typePub.set(batteryData[3])
            mfgPub.set(batteryData[4])
        except:
            print("READ ERROR, RETRYING")
        time.sleep(2)
finally:
    GPIO.cleanup()
