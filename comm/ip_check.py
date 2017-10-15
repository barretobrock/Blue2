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
from comm.commtools import Inet, PBullet
from primary.maintools import Paths
from logger.pylogger import Log


inet = Inet()
p = Paths()
logg = Log('autopi.ip', p.log_dir, 'autopi_ipaddr', log_lvl="DEBUG")
logg.debug('Log initiated')
pb = PBullet(p.key_dict['pushbullet_api'])

with open(p.ip_path) as f:
    last_ip = f.read().replace('\n', '')

if inet.ping_success():
    # If internet connection, check that ip address is the same
    current_ip = inet.ip_addr
    logg.debug('Checked ip: {}'.format(current_ip))
    if last_ip != current_ip:
        # IP address for device has changed. Save new ip address and notify
        logg.debug('IP address changed from {} to {}'.format(last_ip, current_ip))
        pb.send_message(title="IP Address Changed", message="IP address has been changed to {}".format(current_ip))
        with open(p.ip_path, 'w') as f:
            f.write(current_ip)

logg.close()