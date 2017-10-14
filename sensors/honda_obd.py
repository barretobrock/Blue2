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
import obd
import time

connection = obd.OBD()

cmd_dict = {
    'ENGINE_LOAD': obd.commands.ENGINE_LOAD,
    'COOLANT_TEMP': obd.commands.COOLANT_TEMP,
    'SHORT_FUEL_TRIM_1': obd.commands.SHORT_FUEL_TRIM_1,
    'SHORT_FUEL_TRIM_2': obd.commands.SHORT_FUEL_TRIM_2,
    'LONG_FUEL_TRIM_1': obd.commands.LONG_FUEL_TRIM_1,
    'LONG_FUEL_TRIM_2': obd.commands.LONG_FUEL_TRIM_2,
    'FUEL_PRESSURE': obd.commands.FUEL_PRESSURE,
    'INTAKE_PRESSURE': obd.commands.INTAKE_PRESSURE,
    'RPM': obd.commands.RPM
}

prevtime = time.time()
for k, v in cmd_dict:
    response = connection.query(v)
    print("Value for {}: {} in {:.3f} seconds".format(k, response.value, time.time() - prevtime))
    prevtime = time.time()

