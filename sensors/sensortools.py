#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools for reading sensors and transmitting the info
"""
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
    sys.path.insert(0, os.path.join(cur_dir, 'blue2'))
# import custom modules


class TempSensor:
    """
    Sets up a sensor for temperature readings
    Args for __init__:
        model: str, model of temperature sensor ('DHT', 'Dallas')
    """
    def __init__(self, model='Dallas'):
        self.model = model

    def measurement(self, pin):
        readings = {}
        if self.model == 'DHT':
            self.AdaDHT = __import__('Adafruit_DHT')
            sensor = self.AdaDHT.DHT22
            humidity, temp = self.AdaDHT.read_retry(sensor, pin)
            readings = {
                'humidity': humidity,
                'temp': temp,
            }
            for v in readings.keys():
                reading = readings[v]
                if isinstance(reading, float) or isinstance(reading, int):
                    readings['{}_fixed'.format(v)] = round(reading, 1)
        elif self.model == 'Dallas':
            # For Dallas temp sensor, the pin becomes the serial number
            sensor_path = '/sys/bus/w1/devices/{}/w1_slave'.format(pin)
            with open(sensor_path) as f:
                result = f.read()

            # Split result by line break
            result_list = result.split('\n')
            for r in result_list:
                # loop through line breaks and find line with temp
                if 't=' in r:
                    # Isolate temp reading and convert to float
                    temp = float(r[r.index('t=')+2:])/1000
                    break
            readings = {
                'temp': temp,
            }
        return readings


class DistanceSensor:
    def __init__(self):
        print('stuff')


class LightSensor:
    def __init__(self):
        print('stuff')


class SwitchSensor:
    def __init__(self):
        print('stuff')


class DeviceSensor:
    '''
    Returns stats about the device (CPU, memory, etc.)
    '''
    def __init__(self):
        print('stuff')
