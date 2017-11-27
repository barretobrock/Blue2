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
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
import pandas as pd


p = Paths()
logg = Log('speedtest.plotter', p.log_dir, 'speedtest')
logg.debug('Logging initiated')

matplotlib.use('Agg')
speedtest_data_path = os.path.join(p.data_dir, 'speedtest_data.csv')
plot_path = 'speedtest24_{}.png'.format(pd.datetime.now().strftime('%Y-%m-%d'))
# Read in data
data = pd.read_csv(speedtest_data_path)

# filter dataframe to only last 24 hours
now = pd.datetime.now()
last24 = now - pd.Timedelta('1 days')
last24 = last24.isoformat()
data = data[data.TIMESTAMP > last24]

# convert timestamp strings to pd.datetime
data.TIMESTAMP = pd.to_datetime(data.TIMESTAMP)

rcParams['xtick.labelsize'] = 'xx-small'

plt.plot(data.TIMESTAMP, data.DOWNLOAD, 'b-')

plt.axhline(y=20, color='r', linestyle=':')
plt.title('Bandwidth Report (last 24 hours)')
plt.ylabel('Mbps')
plt.xlabel('Timestamp')

plt.yticks(range(0, 31, 5))
plt.ylim(0.0, 30.0)

current_axes = plt.gca()
current_figure = plt.gcf()

hfmt = dates.DateFormatter('%d.%M %H:%M')
current_axes.xaxis.set_major_formatter(hfmt)
current_figure.subplots_adjust(bottom=.25)

loc = current_axes.xaxis.get_major_locator()
loc.maxticks[dates.HOURLY] = 24
loc.maxticks[dates.MINUTELY] = 60

current_figure.savefig(os.path.join(p.data_dir, *['plots', plot_path]))

logg.close()