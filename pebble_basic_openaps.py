import time, datetime, sys, socket, json, libpebble2

#from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
#from libpebble2.exceptions import TimeoutError
#from libpebble2.services.notifications import Notifications


pebble = libpebble2.PebbleConnection(SerialTransport("/dev/rfcomm0"))
pebble.connect()
pebble.run_async()
print(pebble.watch_info.serial)

hostname= socket.gethostname()

with open ("/root/myopenaps/monitor/glucose.json")as BG_Data:
	d= json.load(BG_Data)
	BG=d[0]["glucose"]
	#Time_BG=d[0]["display_time"]
	Time_BG=datetime.datetime.strptime((d[0]["display_time"], "%Y-%m-%dT%H:%M:%S")
	BG_Previous = d[1]["glucose"]
	BG_Delta = BG - BG_Previous

with open ("/root/myopenaps/monitor/iob.json")as IOB_Data:
        d= json.load(IOB_Data)
        IOB=round(d[0]["iob"],1)
    
with open ("/root/myopenaps/monitor/temp_basal.json")as temp_basal_Data:
        d= json.load(temp_basal_Data)
        temp_basal=round(d["rate"],1)


Time_Gap_Minutes = (datetime.datetime.now()-Time_BG).total_seconds()/60

if Time_Gap_Minutes < 15:

	msg_line1= str(BG) + "(" + str(BG_Delta) +  ")/" + str(IOB) + "/" + str(temp_basal)
	msg_line2= str(Time_BG_py)[11:16]
	
else:
	msg_line1 = "Old Data: " + str(Time_Gap_Minutes) + "m"
	msg_line2 = str(BG) + "(" + str(BG_Delta) +  ")/" + str(IOB) + "/" + str(temp_basal)

libpebble2.Notifications(pebble).send_notification(msg_line1, msg_line2)
#Notifications(pebble).send_notification(sys.argv[1], sys.argv[2])

print ("----------")
print (msg_line1)
print (msg_line2)
print ("----------")
