# pebble_basic_openaps

Sending basic update messages to pebble from an openaps rig

Messages are recieved in pebble watch as notifications

Takes advantage of small pebble displays such as newer timeround models

Simple aletrnative to have just the critical information in the pebble. Meant to be added as a cronjob every 5 min

**I am in the innital testing of this idea**

The intended message in the pebble contains two lines:

        Line 1: BG(BG Delta)/IOB/Temp Basal
        Line 2: BG time, then between parenthesis the time elapsed from BG time to now expressed in minutes
  
example below:

        ----------
        82(-1)/-0.583/0.0
        10:27 (1min.)
        ----------

If the time elapsed from the last BG time is more than 25 minutes the message will be different:

        Line 1: Data is <Time elapsed from BG time to now expressed in minutes> Old
        Line 2: hostname
        
example below:

        ----------
        Data is 35m Old
        Edison1
        ----------


#Dependencies:

        Openaps
        Bluez
        Libpebble2

#Startup

        nfig hci0 up
        systemctl start bluetooth.service #(part of pancreable instructions..not sure what this is for)
        rfcomm bind hci0 B0:B4:48:F4:F0:C5 #this links to the MAC of the pebble watch

