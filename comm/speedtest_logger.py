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
    sys.path.insert(0, os.path.join(cur_dir, 'blue2'))
# import custom modules
from speedtest import Speedtest
import pandas as pd
from logger.pylogger import Log
from primary.maintools import Paths


p = Paths()
logg = Log('speedtest.logger', p.log_dir, 'speedtest')
logg.debug('Logging initiated')

# Load previous data
save_path = os.path.join(p.data_dir, 'speedtest_data.csv')

# Prep speedtest by getting nearby servers
speed = Speedtest()
speed.get_servers([])
speed.get_best_server()

down = speed.download()/1000000
up = speed.upload()/1000000

# put variables into pandas type dataframe
test = pd.DataFrame({
    'TIMESTAMP': pd.datetime.now().isoformat(),
    'DOWNLOAD': down,
    'UPLOAD': up,
}, index=[0])

# Append data to csv file
if os.path.exists(save_path):
    # Append
    test.to_csv(save_path, mode='a', header=False)
else:
    # Write
    test.to_csv(save_path)

logg.close()
