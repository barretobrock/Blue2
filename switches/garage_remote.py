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
    sys.path.insert(0, os.path.join(cur_dir, *['Scripts', 'blue2']))
# import custom modules
from Global.maintools import Paths
from Global.commtools import DomoticzComm


p = Paths()
dc = DomoticzComm(p.garagepi_ip)

# ID of sensor in Domoticz
sensor_id = 1
# Switch type is push-on, so changing status requires it to be turned on
dc.switch_on(sensor_id)
