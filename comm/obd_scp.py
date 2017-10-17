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
    sys.path.insert(0, cur_dir)
# import custom modules
from primary.maintools import Paths
from comm.commtools import PBullet
from logger.pylogger import Log
import glob

p = Paths()
logg = Log('obd.uploader', p.log_dir, 'obd_uploader', log_lvl="DEBUG")
pb = PBullet(p.key_dict['pushbullet_api'])
target_dir = os.path.abspath('/home/{}/data'.format(p.server_hostname))

# find most recent csv file in data folder
list_of_files = glob.glob("{}*.csv".format(p.data_dir))
logg.debug('{} files total.'.format(len(list_of_files)))
if len(list_of_files) > 0:
    for csvfile in list_of_files:
        # Upload files to server computer
        cmd = "scp {} {}@{}:{}".format(os.path.join(p.data_dir, csvfile), p.server_hostname,
                                       p.server_ip, os.path.join(target_dir, csvfile))
        response = os.system(cmd)
        if response == 0:
            pb.send_mesage("File successfully sent.", "The data file was successfully sent.")
            logg.debug('Successfully uploaded {}'.format(os.path.basename(csvfile)))
            # File was successfully transmitted; remove file
            rm_cmd = "rm {}".format(csvfile)
            response1 = os.system(rm_cmd)
        else:
            pb.send_mesage("Error in uploading files.", "Error in uploading csv files.")

logg.close()
