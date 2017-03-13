import time, sys, socket, json, datetime

from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.exceptions import TimeoutError
from libpebble2.services.notifications import Notifications

pebble = PebbleConnection(SerialTransport("/dev/rfcomm0"))
pebble.connect()
pebble.run_async()

print(pebble.watch_info.serial)

hostname= socket.gethostname()

with open ("/root/myopenaps/monitor/glucose.json")as BG_Data:
	d= json.load(BG_Data)
	BG=d[0]["glucose"]
	Time_BG=datetime.datetime.strptime((d[0]["display_time"])[0:19], "%Y-%m-%dT%H:%M:%S")
	BG_previous=d[1]["glucose"]
	BG_Delta = BG - BG_previous
	if BG_Delta > 0:
		BG_Delta_str = "+" + str(BG_Delta)
	else:
		BG_DElta_str = str (BG_Delta)
	Time_Gap_Minutes = (datetime.datetime.now()-Time_BG).total_seconds()/60
	if Time_Gap_Minutes < 60:
		Time_Gap_str = str(int(Time_Gap_Minutes)) + "m"
	else:
		Time_Gap_str = str(float(Time_Gap_Minutes / 60)) + "hr"

with open ("/root/myopenaps/monitor/iob.json")as IOB_Data:
        d= json.load(IOB_Data)
        IOB=round(d[0]["iob"],1)
    
with open ("/root/myopenaps/monitor/temp_basal.json")as temp_basal_Data:
        d= json.load(temp_basal_Data)
        temp_basal=str(round(d["rate"],1))


with open ("/root/myopenaps/monitor/status.json")as Status_Data:
        d= json.load(Status_Data)
        Suspended=d["suspended"]
	if Suspended == True:
		temp_basal = "Sus"

with open ("/root/myopenaps/monitor/edison-battery.json")as Edison_Battery_Data:
	d= json.load(Edison_Battery_Data)
	Edison_Battery=d["battery"]
	Edison_Battery_str= "[" + "*" * int(Edison_Battery/20) + " " * (5-int(Edison_Battery/20))+ "]" 

with open ("/root/myopenaps/monitor/reservoir.json")as Reservoir_Data:
        d= json.load(Reservoir_Data)
	Reservoir = int(d)
        Reservoir_str=str(Reservoir)+"u"
	      

if Time_Gap_Minutes < 15:

	msg_line1= str(BG) + "(" + BG_Delta_str +  ")/" + str(IOB) + "/" + temp_basal
	msg_line2= Reservoir_str + " " + Edison_Battery_str
   
else:
	msg_line1 = "Old Data: " + Time_Gap_str
	msg_line2 = ""


Notifications(pebble).send_notification(msg_line1, msg_line2)
#Notifications(pebble).send_notification(sys.argv[1], sys.argv[2])

print ("----------")
print (msg_line1)
print (msg_line2)
print ("----------")
