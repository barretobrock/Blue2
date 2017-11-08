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
from primary.maintools import Paths, CSVHelper
from logger.pylogger import Log


p = Paths()
logg = Log('obd.compacter', p.log_dir, 'obd_compacter', log_lvl="DEBUG")
logg.debug('Log initiated')

csvhelp = CSVHelper()

# Set path to compact csv files to
compact_path = os.path.join(p.data_dir, 'obd_results_main.csv')
file_glob = os.path.join(p.data_dir, 'obd_results_201*.csv')

# Compact the csv files
csvhelp.csv_compacter(compact_path, file_glob, sort_column='TIMESTAMP')

logg.debug('File compaction completed.')

logg.close()
