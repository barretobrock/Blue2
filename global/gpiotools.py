#!/usr/bin/env python3
import RPi.GPIO as GPIO


class BCM:
    def __init__(self, pin):
        self.pin = pin
        # Disable warnings
        GPIO.setwarnings(False)
        # Use 'gpio readall' to get BCM pin layout for RasPi model
        GPIO.setmode(GPIO.BCM)

    def cleanup(self, pin=None):
        if pin is None:
            GPIO.cleanup()
        else:
            GPIO.cleanup(pin)

