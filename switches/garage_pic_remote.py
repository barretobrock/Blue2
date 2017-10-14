#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import socket
home_dir = os.path.expanduser("~")
hostname = socket.gethostname()
# If on Macbook, add path to blue2 from Dropbox, otherwise add from home directory
if 'macbook' in hostname.lower():
    # In case debugging from Macbook
    home_dir = os.path.join(home_dir, *['Dropbox', 'Programming', 'Scripts'])

blue2_dir = os.path.join(home_dir, 'blue2')
if blue2_dir not in sys.path:
    sys.path.append(blue2_dir)
# import custom modules
from Global.maintools import Paths
from Global.commtools import DomoticzComm


p = Paths()
dc = DomoticzComm(p.garagepi_ip)

# ID of sensor in local Domoticz
sensor_id = 2
# Switch type is push-on, so changing status requires it to be turned on
dc.switch_on(sensor_id)
