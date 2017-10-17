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
import RPi.GPIO as GPIO
import time


class Pulse:
    def __init__(self, pin):
        self.pin = pin
        # setup GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # setup pin
        GPIO.setup(self.pin, GPIO.OUT, initial=0)

    def do_pulse(self, n, s=0.05):
        for i in range(n):
            # set pin to high
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(s)
            # set pin to low
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(s)
        GPIO.cleanup(self.pin)
