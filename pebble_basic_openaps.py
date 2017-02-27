import time
import sys
import socket
import json
import datetime

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
	Time_BG=d[0]["display_time"]
	BG_Previous = d[1]["glucose"]
	BG_Delta = BG - BG_Previous

with open ("/root/myopenaps/monitor/iob.json")as IOB_Data:
        d= json.load(IOB_Data)
        IOB=round(d[0]["iob"],1)
    
with open ("/root/myopenaps/monitor/temp_basal.json")as temp_basal_Data:
        d= json.load(temp_basal_Data)
        temp_basal=round(d["rate"],1)


Time_BG=Time_BG.replace("T", " ")
Time_BG=Time_BG[0:19]
Time_BG_py=datetime.datetime.strptime(Time_BG, "%Y-%m-%d %H:%M:%S")


Time_Gap = datetime.datetime.now()-Time_BG_py
(h, m, s) = str(Time_Gap).split(":")
Time_Gap_Min = int(h)/60+int(m)


msg_line1= str(Time_BG[11:16]) + " (" + str(Time_Gap_Min) + "min.)"



if Time_Gap_Min < 25:

	msg_line2= str(Time_BG[11:16]) + " (" + str(Time_Gap_Min) + "m)"
	msg_line1= str(BG) + "(" + str(BG_Delta) +  ")/" + str(IOB) + "/" + str(temp_basal)
	
else:
	msg_line2 = "Data " + str(Time_Gap_Min) + "m Old"
	msg_line1 = hostname

Notifications(pebble).send_notification(msg_line1, msg_line2)
#Notifications(pebble).send_notification(sys.argv[1], sys.argv[2])

print ("----------")
print (msg_line1)
print (msg_line2)
print ("----------")
