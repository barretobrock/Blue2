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
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go
import json


def dow_boxplot(df, data_col, dow_col, save_dir, incl_weekend=False, plot_online=False):
    """
    Uses plotly package to graph a box plot + mean line graph of data,
        grouped by day of week (DOW)
    Args:
        df: pandas.DataFrame containing the data
        data_col: str, column name containing the data to examine
        dow_col: column name containing the day of week
        save_dir: directory to save image/html file to
        incl_weekend: boolean, include weekend days in graph
    """

    title_portion = data_col.replace('_', ' ').title()
    file_name = '{}_graph'.format(data_col)
    png_file_path = os.path.join(save_dir, '{}.png'.format(file_name))

    marker_dict = {
        'size': 10,
        'color': 'rgba(255, 182, 193, .9)',
        'line': {
            'width': 2
        }
    }

    # Sort by DOW
    df['dow'] = df['dow'].astype(int)
    df = df.sort_values(by=dow_col)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    if not incl_weekend:
        # Remove weekend days
        df = df[df[dow_col] < 6]
        days = days[:5]

    # Get mean for each DOW
    mean_by_dow = df.groupby(by=dow_col)[data_col].mean()
    # Begin populating data list
    data = []
    for d in df[dow_col].unique().tolist():
        data.append(go.Box(y=df[df[dow_col] == d][data_col], name=days[d - 1], showlegend=False))

    data.append(go.Scatter(x=days, y=mean_by_dow, mode='lines+markers', name='mean', marker=marker_dict))

    if 'hour' in data_col:
        yax_title = 'Time Worked (hrs)'
    else:
        yax_title = 'Commute Time (mins)'

    layout = go.Layout(
        title='{} Stats by Day'.format(title_portion),
        xaxis={
            'title': 'Day of Week',
        },
        yaxis={
            'title': yax_title,
        },
        width=800,
        height=640
    )
    fig = go.Figure(data=data, layout=layout)

    py.image.save_as(fig, filename=png_file_path)
    if plot_online:
        # Save plot online (to put on website)
        py.plot(fig, filename=file_name)


p = Paths()
logg = Log('commute.grapher', p.log_dir, 'commute', log_lvl="DEBUG")
logg.debug('Log initiated')

api = json.loads(p.key_dict['plotly_api'])

csv_path = os.path.join(p.data_dir, 'commute_calculations.csv')
# Import csv data
commute_df = pd.read_csv(csv_path, index_col=0, delimiter=',', lineterminator='\n')

# Read in pyplot credentials
py.sign_in(username=api['username'], api_key=api['api_key'])

dow_boxplot(commute_df, 'work_commute', 'dow', p.data_dir, incl_weekend=False, plot_online=True)
dow_boxplot(commute_df, 'hours_at_work', 'dow', p.data_dir, incl_weekend=False, plot_online=True)
dow_boxplot(commute_df, 'home_commute', 'dow', p.data_dir, incl_weekend=False, plot_online=True)

logg.close()