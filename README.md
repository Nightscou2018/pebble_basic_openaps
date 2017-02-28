# pebble_basic_openaps

Sending basic update messages to pebble from an openaps rig

Tested so far with an Edison/Explorer rig

Messages are recieved in the pebble as notifications

Takes advantage of small pebble displays such as newer timeround models

Simple aletrnative to have just the critical information in the pebble. Meant to be added as a cronjob every 5 min

![alt tag](https://github.com/betluis/pebble_basic_openaps/blob/master/picture.JPG)


**I am in the innital testing and iterating of this idea**

The intended message in the pebble contains two lines:

        Line 1: BG(BG Delta)/IOB/Temp Basal
        Line 2: BG time, then between parenthesis the time elapsed from BG time to now expressed in minutes
  
example below:

        ----------
        82(-1)/-0.5/0.0
        10:27 (1m)
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

#Run before sending messages to the pebble 

        nfig hci0 up
        systemctl start bluetooth.service 
        rfcomm bind hci0 B0:B4:48:F4:F0:C5 #replace the MAC address with that of your pebble

Add as a startup script


