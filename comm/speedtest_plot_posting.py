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
from logger.pylogger import Log
from primary.maintools import Paths
from comm.commtools import Twitter
import pandas as pd


p = Paths()
logg = Log('twitkov.speedtest_plot', p.log_dir, 'personal_twitter')
logg.debug('Logging initiated')

tweepy_dict = eval(p.key_dict['personal_tweepy_api'])
tw = Twitter(tweepy_dict)

# Load graph pic
plot_path = 'speedtest24_{}.png'.format(pd.datetime.now().strftime('%Y-%m-%d'))


char_limit = 280

plot_fullpath = os.path.join(p.data_dir, *['plots', plot_path])
if os.path.exists(plot_fullpath):
    status_txt = "Results are in for the last 24 hours of bandwidth! #speedtest #bandwidth #download"
    tw.update_with_media(plot_fullpath, status=status_txt)
else:
    logg.debug("Plot picture could not be found. No status update was made.")

logg.close()
