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
#from comm.commtools import Camera, PBullet
from primary.maintools import Paths

p = Paths()
c = Camera()
pb = PBullet(p.pushbullet_api)

imgpath = c.capture_image(p.image_dir, vflip=True, hflip=True)
pb.send_img(imgpath, os.path.basename(imgpath), 'image/png')

