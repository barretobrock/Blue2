#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BCM:
    """
    Connects to GPIO on Raspberry Pi
    Args for __init__:
        pin: int, BCM pin on GPIO
    """
    def __init__(self, pin):
        rpi = __import__('RPi')
        self.GPIO = rpi.GPIO
        self.pin = pin
        # Disable warnings
        self.GPIO.setwarnings(False)
        # Use 'gpio readall' to get BCM pin layout for RasPi model
        self.GPIO.setmode(self.GPIO.BCM)

    def cleanup(self, pin=None):
        """Resets GPIO by pin or for entire board"""
        if pin is None:
            self.GPIO.cleanup()
        else:
            self.GPIO.cleanup(pin)

