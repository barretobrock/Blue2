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
    sys.path.insert(0, os.path.join(cur_dir, *['Scripts', 'blue2']))
# import custom modules
from comm.commtools import Inet, PBullet
from primary.maintools import Paths
from logger.pylogger import Log


p = Paths()
logg = Log('autopi.ip', p.log_dir, 'autopi_ipaddr', log_lvl="DEBUG")
logg.debug('Log initiated')

inet = Inet()

pb = PBullet(p.key_dict['pushbullet_api'])

with open(p.ip_path) as f:
    last_ip = f.read().replace('\n', '')

if inet.ping_success():
    # If internet connection, check that ip address is the same
    current_ip = inet.get_ip_address()
    if current_ip != '':
        logg.debug('Checked ip: {}'.format(current_ip))
        if last_ip != current_ip:
            # IP address for device has changed. Save new ip address and notify
            logg.debug('IP address changed from {} to {}'.format(last_ip, current_ip))
            pb.send_message(title="IP Address Changed", message="IP address has been changed to {}".format(current_ip))
            with open(p.ip_path, 'w') as f:
                f.write(current_ip)

logg.close()

