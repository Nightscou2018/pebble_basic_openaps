# pebble_basic_openaps

Sending basic update messages to pebble from an openaps rig

When using Medtronic CGM (without an additional device to see BG) it gives the patient a practical way to stay on top of key information without the hassle of accessing the pump.

Particularly useful when offline or if opening NightScout is not practical or desired for any reason
 
Tested so far with an Edison/Explorer rig

Messages are received in the pebble as notifications

Takes advantage of small pebble displays such as newer timeround models

Meant to be added as a cronjob every 5 min (or as often as you want, I am testing with 1 min updates)

In the pebble you can define how many minutes the message stays current. After that time (I have it as 3 min for now), the watch sends you to the updates list, where you can scroll down through previous messages. This functionality gives you a quick way to know if your data is current and also to explore recent values.


![alt tag](https://github.com/betluis/pebble_basic_openaps/blob/master/picture.JPG)


**I am in the initial testing and iterating of this idea**

The intended message in the pebble contains two lines:

        Line 1: BG(BG Delta)/IOB/Temp Basal
        Line 2: BG time, then between parenthesis the time elapsed from BG time to now expressed in minutes
  
Example below:

        ----------
        82(-1)/-0.5/0.0
        10:27 (1m)
        ----------

If the time elapsed from the last BG time is more than 15 minutes (normally glucose data in Openaps is updated every 5 min) the message will be different:

        Line 1: Old Data: <Time elapsed from BG time to now expressed in minutes>
        Line 2: BG(BG Delta)/IOB/Temp Basal
        
Example below:

        ----------
        Old Data: 35m 
        82(-1)/-0.5/0.0
        ----------

#Dependencies:

Openaps

Bluez

        sudo apt-get install bluez
        
        to pair your watch, look at section: "using bluetoothctl" of instructions in the next link
        https://wiki.debian.org/BluetoothUser
                
Libpebble2

        pip install libpebble2

#Run before sending messages to the pebble 

        hciconfig hci0 up
        systemctl start bluetooth.service 
        rfcomm bind hci0 B0:B4:48:F4:F0:C5 #replace the MAC address with that of your pebble

Add as a startup script

#To do

Take advantage of Openaps Oref0 set up script to facilitate Bluetooth configuration







