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
from primary.maintools import Paths
from sensors.sensortools import TempSensor
from comm.commtools import DomoticzComm


p = Paths()
dc = DomoticzComm(p.mainpi_ip)
tsensor = TempSensor('Dallas')
# Serial number of temp sensor
sensor_serial = '28-0000079aefc4'
# ID of sensor in Domoticz
sensor_id = 8

temp_dict = tsensor.measurement(sensor_serial)
temp = temp_dict['temp']

dc.send_sensor_data(sensor_id, temp)
