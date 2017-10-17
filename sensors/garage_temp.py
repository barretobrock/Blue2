#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os
import sys
import socket
# set system paths for importing custom modules/functions
cur_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
hostname = socket.gethostname()
if '__file__' in globals():
    # if not running in debugger, assign parent directory of file to system paths
    parent_dir = os.path.dirname(os.path.dirname(cur_dir))
    sys.path.insert(0, os.path.join(parent_dir, 'blue2'))
else:
    # otherwise set system paths based on project directory in PyCharm
    sys.path.insert(0, cur_dir)
# import custom modules
from primary.maintools import Paths
from sensors.sensortools import TempSensor
from comm.commtools import DomoticzComm


p = Paths()
dc = DomoticzComm(p.mainpi_ip)
tsensor = TempSensor('Dallas')
# Serial number of temp sensor
sensor_serial = '28-0000079b32f9'
# ID of sensor in Domoticz
sensor_id = 7

temp_dict = tsensor.measurement(sensor_serial)
temp = temp_dict['temp']

dc.send_sensor_data(sensor_id, temp)



