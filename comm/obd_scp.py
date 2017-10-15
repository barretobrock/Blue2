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
from primary.maintools import Paths
from comm.commtools import PBullet
import glob

p = Paths()
pb = PBullet(p.key_dict['pushbullet_api'])
target_dir = os.path.abspath('/home/{}/data'.format(p.server_hostname))

# find most recent csv file in data folder
list_of_files = glob.glob("{}*.csv".format(p.data_dir))
if len(list_of_files) > 0:
    for csvfile in list_of_files:
        # Upload files to server computer
        cmd = "scp {} {}@{}:{}".format(os.path.join(p.data_dir, csvfile), p.server_hostname,
                                       p.server_ip, os.path.join(target_dir, csvfile))
        response = os.system(cmd)
        if response == 0:
            pb.send_mesage("File successfully sent.", "The data file was successfully sent.")
            # File was successfully transmitted; remove file
            rm_cmd = "rm {}".format(csvfile)
            response1 = os.system(rm_cmd)
        else:
            pb.send_mesage("Error in uploading files.", "Error in uploading csv files.")
