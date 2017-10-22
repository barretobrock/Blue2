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
from primary.maintools import Paths
#from comm.commtools import PBullet
from logger.pylogger import Log
import glob
import paramiko
from scp import SCPClient

p = Paths()
logg = Log('obd.uploader', p.log_dir, 'obd_uploader', log_lvl="DEBUG")
logg.debug('Log initiated')

# Set location for RSA key
privatekey_path = os.path.join(p.home_dir, *['.ssh', 'id_rsa'])
mkey = paramiko.RSAKey.from_private_key_file(privatekey_path)

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(p.server_ip, username=p.server_hostname, pkey=mkey)
#scp = SCPClient(ssh.get_transport())
sftp = ssh.open_sftp()

#pb = PBullet(p.key_dict['pushbullet_api'])
target_dir = os.path.abspath('/home/{}/data'.format(p.server_hostname))

# find most recent csv file in data folder
list_of_files = glob.glob("{}/*.csv".format(p.data_dir))
logg.debug('{} files total.'.format(len(list_of_files)))
if len(list_of_files) > 0:
    for csvfile in list_of_files:
        target_path = os.path.join(target_dir, os.path.basename(csvfile))
        sftp.put(csvfile, target_path)
        logg.debug('Successfully uploaded {}'.format(os.path.basename(csvfile)))
        if '2' in csvfile:
            try:
                os.remove(csvfile)
            except OSError:
                pass

logg.close()
