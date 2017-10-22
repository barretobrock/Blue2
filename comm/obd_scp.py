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
from logger.pylogger import Log
import glob
import paramiko


p = Paths()
logg = Log('obd.uploader', p.log_dir, 'obd_uploader', log_lvl="DEBUG")
logg.debug('Log initiated')

# Set location for RSA key
privatekey_path = os.path.join(p.home_dir, *['.ssh', 'id_rsa'])
mkey = paramiko.RSAKey.from_private_key_file(privatekey_path)

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to server using private key
ssh.connect(p.server_ip, username=p.server_hostname, pkey=mkey)

sftp = ssh.open_sftp()
# Set directory to put csv files after transfer to server computer
target_dir = os.path.abspath('/home/{}/data'.format(p.server_hostname))

# Find all csv files in data folder relating to obd
list_of_files = glob.glob("{}/obd_results*.csv".format(p.data_dir))
logg.debug('{} files total. Beginning transfer.'.format(len(list_of_files)))
if len(list_of_files) > 0:
    for csvfile in list_of_files:
        target_path = os.path.join(target_dir, os.path.basename(csvfile))
        # Transfer file
        sftp.put(csvfile, target_path)
        logg.debug('Successfully uploaded {}'.format(os.path.basename(csvfile)))
        try:
            # Try to remove file after successful transfer
            os.remove(csvfile)
        except OSError:
            pass

logg.close()
