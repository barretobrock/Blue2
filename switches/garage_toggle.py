#!/usr/bin/env python3
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
    sys.path.insert(0, os.path.join(parent_dir, 'Scripts'))
else:
    # otherwise set system paths based on project directory in PyCharm
    sys.path.insert(0, cur_dir)
if any([name in hostname for name in ['MacBook', 'buntu']]):
    # In case debugging from laptops :)
    sys.path.insert(0, os.path.join(*[cur_dir, 'Scripts', 'LPBOT', 'Scripts']))
else:
    sys.path.insert(0, os.path.join(*[cur_dir, 'LPBOT', 'Scripts']))
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
