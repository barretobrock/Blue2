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
from comm.commtools import PBullet
import gspread
from collections import OrderedDict
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def grab_timestamp(activity, location, avg_time_str):
    avg_time = pd.to_datetime(avg_time_str, format="%H:%M")
    adjusted = False
    try:
        # Get the timestamp when I left home
        tmstmp = df[(df['activity'] == activity) & (df['Location'] == location)].iloc[0].timestamp
    except IndexError:
        # If time left home not recorded, give the average time
        #   TODO calculate the average time left for non-zero results
        tmstmp = pd.to_datetime(row['date']).replace(hour=avg_time.hour, minute=avg_time.minute)
        adjusted = True
    return {'tstamp': tmstmp, 'adjusted': adjusted}


def seconds_since_midnight(timestamp):
    seconds = (timestamp - timestamp.replace(hour=0, minute=0, second=0)).total_seconds()
    return seconds

p = Paths()
pb = PBullet(p.key_dict['pushbullet_api'])
client_secret_path = p.google_client_secret

csv_save_path = os.path.join(p.data_dir, 'commute_calculations.csv')

# Use creds to create a client to interact with Google Sheets API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_path, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
ws = client.open("Movement At Location")
sheet = ws.sheet1
processed_sheet = ws.worksheet('Processed')

# Check when the file was last updated
last_update = processed_sheet.cell(1, 2).value

commute_df = pd.DataFrame(sheet.get_all_records())

# Begin processing columns
# First, Date columns
commute_df['timestamp'] = pd.to_datetime(commute_df['Raw_date'], format='%B %d, %Y at %I:%M%p')
last_entry = max(commute_df['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

if last_update < last_entry:
    # New entry found, rerun calculations
    now = pd.datetime.now()
    # Refactor arrival/departure column
    commute_df['activity'] = ''
    commute_df.loc[commute_df.Activity == 'Left location', ['activity']] = 'left'
    commute_df.loc[commute_df.Activity == 'Arrived at location', ['activity']] = 'arrived'
    # Take out unused columns
    commute_df = commute_df[['activity', 'Location', 'timestamp']]
    # Determine work day [1 = Monday, 7 = Sunday]
    commute_df['date'] = commute_df.timestamp.apply(lambda x: x.date())

    min_date = min(commute_df['date'])
    max_date = max(commute_df['date'])
    date_range = pd.date_range(start=min_date, end=max_date)

    daily_commute_df = pd.DataFrame(OrderedDict((
        {
            'date': date_range.date,
            'dow': date_range.strftime('%u'),
            'adjusted_work_commute': False,
            'work_commute': 0,
            'hours_at_work': 0,
            'adjusted_home_commute': False,
            'home_commute': 0
        }))
    )

    for i in range(daily_commute_df.shape[0]):
        row = daily_commute_df.iloc[i]
        if int(row['dow']) < 6:
            # work day
            df = commute_df[commute_df['date'] == row['date']]
            time_left_home = grab_timestamp('left', 'HOME', '07:35')
            time_arrived_work = grab_timestamp('arrived', 'BAO_WORK', '08:25')
            time_left_work = grab_timestamp('left', 'BAO_WORK', '16:45')
            time_arrived_home = grab_timestamp('arrived', 'HOME', '17:30')
            # Calculate minutes for work commute
            row['work_commute'] = pd.Timedelta(time_arrived_work['tstamp'] - time_left_home['tstamp']).seconds / 60
            row['adjusted_work_commute'] = any([time_left_home['adjusted'], time_arrived_work['adjusted']])
            row['hours_at_work'] = pd.Timedelta(time_left_work['tstamp'] - time_arrived_work['tstamp']).seconds / 60 / 60
            row['home_commute'] = pd.Timedelta(time_arrived_home['tstamp'] - time_left_work['tstamp']).seconds / 60
            row['adjusted_home_commute'] = any([time_left_work['adjusted'], time_arrived_home['adjusted']])
            # Merge row back in with data frame
            daily_commute_df.iloc[i] = row

    # Save csv file
    daily_commute_df.to_csv(csv_save_path)

    # Loop through daily_commute_df and add to processed sheet
    #for i in range(daily_commute_df.shape[0]):
    #    for j in range(daily_commute_df.shape[1]):

    # Notify of my recent commute time
    latest_entry = commute_df[commute_df['timestamp'] == max(commute_df['timestamp'])]
    today_df = daily_commute_df[daily_commute_df['date'] == now.date()]
    msg = ''

    if all([latest_entry['activity'] == 'arrived', latest_entry['Location'] == 'BAO_WORK']):
        # Just arrived at work, analyze commute times
        avg_commute = daily_commute_df[(daily_commute_df['work_commute'] > 0) & (-daily_commute_df['adjusted_work_commute'])][
                'work_commute'].mean()
        commute_time = today_df['work_commute'].iloc[0]
        commute_diff = commute_time - avg_commute
        # Generate message
        msg = """
        Woah! You just got to work! Awesome! Here are your stats:\n
        Commute Time: {:.2f} mins
        Average: {:10.2f} mins
        ------------------------
        Difference: {:+7.2f} mins
        """.format(commute_time, avg_commute, commute_diff)
    elif all([latest_entry['activity'] == 'left', latest_entry['Location'] == 'BAO_WORK']):
        # Just arrived at work, analyze commute times
        avg_commute = daily_commute_df[(daily_commute_df['hours_at_work'] > 0)]['hours_at_work'].mean()
        commute_time = today_df['hours_at_work'].iloc[0]
        commute_diff = commute_time - avg_commute
        # Generate message
        msg = """
        Woah! You just left work! Awesome! Here are your stats:\n
        Work Time: {:6.2f} hrs
        Average: {:8.2f} hrs
        ------------------------
        Difference: {:+5.2f} hrs
        """.format(commute_time, avg_commute, commute_diff)
    elif all([latest_entry['activity'] == 'arrived', latest_entry['Location'] == 'HOME']):
        # Just arrived at work, analyze commute times
        avg_commute = daily_commute_df[(daily_commute_df['home_commute'] > 0) & (-daily_commute_df['adjusted_home_commute'])][
                'home_commute'].mean()
        commute_time = today_df['home_commute'].iloc[0]
        commute_diff = commute_time - avg_commute
        # Generate message
        msg = """
        Woah! You just got home! Awesome!
        Here are your stats:\n
        Commute: {:5.2f} mins
        Average: {:10.2f} mins
        -----------------------------------
        Difference: {:+7.2f} mins
        """.format(commute_time, avg_commute, commute_diff)

    if msg != '':
        pb.send_message('Commute Calculations', msg)

    # Update cell with timestamp
    processed_sheet.update_cell(1, 2, pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


