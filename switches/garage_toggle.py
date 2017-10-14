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

# BCM pin
RELAY_PIN = 21
# Duration relay state is reversed from unenergized (depending on connection)
OFF_DELAY = 1

# setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setup pin
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)

# toggle relay
GPIO.output(RELAY_PIN, GPIO.OUT)
time.sleep(OFF_DELAY)
GPIO.output(RELAY_PIN, GPIO.HIGH)

GPIO.cleanup()
