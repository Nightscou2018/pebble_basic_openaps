# pebble_basic_openaps

Sending basic update messages to pebble from an openaps rig

Takes advantage of small pebble displays such as newer timeround models

Simple aletrnative to have just the critical information in the pebble. Meant to be added as a cronjob every 5 min

**/***I am in the innital testing of this idea**

The intended message in the pebble contains two lines:

        Line 1: BG time, then between parenthesis the time elapsed from BG time to now expressed in minutes
        Line 2: BG/IOB/Temp Basal

example below:

        ----------
        10:27 (1min.)
        82/-0.583/0.0
        ----------

If the time elapsed from the last BG time is more than 25 minutes the second line of the message will be different:

        Line 1: BG time, then between parenthesis the time elapsed from BG time to now expressed in minutes
        Line 2: Time since last BG expressed in min -> check why (hostname)
        
example below:

        ----------
        10:27 (35min.)
        35min->check why (Edison1)
        ----------


#Dependencies:

        Openaps
        Bluez
        Libpebble2

#Startup

        nfig hci0 up
        systemctl start bluetooth.service #(part of pancreable instructions..not sure what this is for)
        rfcomm bind hci0 B0:B4:48:F4:F0:C5 #this links to the MAC of the pebble watch

#Pebble_Basic_Openaps.py

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

        with open ("/root/myopenaps/monitor/iob.json")as IOB_Data:
                d= json.load(IOB_Data)
                IOB=d[0]["iob"]
                IOB=round(IOB,2)

        with open ("/root/myopenaps/monitor/temp_basal.json")as temp_basal_Data:
                d= json.load(temp_basal_Data)
                temp_basal=d["rate"]
                temp_basal_ruation=d["duration"]
        
        Time_BG=Time_BG.replace("T", " ")
        Time_BG=Time_BG[0:19]
        Time_BG_py=datetime.datetime.strptime(Time_BG, "%Y-%m-%d %H:%M:%S")
        Time_Gap = datetime.datetime.now()-Time_BG_py
        (h, m, s) = str(Time_Gap).split(":")
        Time_Gap_Min = int(h)/60+int(m)

        msg_line1= str(Time_BG[11:16]) + " (" + str(Time_Gap_Min) + "min.)"
        
        if Time_Gap_Min < 25:
                msg_line2= str(BG) + "/" + str(IOB) + "/" + str(temp_basal)
        else:
                msg_line2 = str(Time_Gap_Min) + "min" + "->check why" + " (" + hostname + ")"

        Notifications(pebble).send_notification(msg_line1, msg_line2)

        print ("----------")
        print (msg_line1)
        print (msg_line2)
        print ("----------")
