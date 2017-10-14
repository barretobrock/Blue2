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
