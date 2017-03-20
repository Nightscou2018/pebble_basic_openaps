Adding parameters in case one wants to run the routine without calling the pebble

The intention is to see the message in the terminal but in case pebbble is not reachable we avoid a timeout error
requires parameter 0 for skipping calling the pebble, anything else will call it
example

     p.py 0
     p.py 1



