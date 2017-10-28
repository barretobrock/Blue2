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
from logger.pylogger import Log
import gspread
from collections import OrderedDict
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def grab_timestamp(daily_df, activity, location, avg_time_str):
    """
    Searches through dataframe for certain activity at certain location.
    If no timestamp found for given combination, the average time string is processed
    Args:
        daily_df: pandas.DataFrame of day's activities at given locations
        activity: str, 'left' or 'arrived'
        location: str, location of activity
        avg_time_str: str, HH:MM of when activity at location takes place on average
    Returns:
        dictionary including timestamp and boolean whether the average time
            was used instead of the actual time.
    """
    avg_time = pd.to_datetime(avg_time_str, format="%H:%M")
    adjusted = False

    # Filter dataframe basec on activity and location
    filtered_df = daily_df[(daily_df['activity'] == activity) & (daily_df['Location'] == location)]

    if not filtered_df.empty:
        # If multiple results in filtered dataframe, apply logic to choose correctly:
        #   activity = 'left': pick first entry
        #   activity = 'arrived': pick last entry
        if filtered_df.shape[0] > 1:
            if activity == 'left':
                xrow = 0
            elif activity == 'arrived':
                xrow = filtered_df.shape[0] - 1
        else:
            xrow = 0
        tmstmp = filtered_df.iloc[xrow]['timestamp']
    else:
        tmstmp = pd.to_datetime(daily_df.iloc[0]['date']).replace(hour=avg_time.hour, minute=avg_time.minute)
        adjusted = True
    return {'tstamp': tmstmp, 'adjusted': adjusted}




def get_metrics(df, todaydf, col_name, incl_adjusted):
    filtered_df = df[(df[col_name] > 0)]
    if not incl_adjusted:
        adj_col_name = 'adjusted_' + col_name
        if adj_col_name in filtered_df.columns:
            filtered_df = filtered_df[(-filtered_df[adj_col_name])]

    filtered_metric = filtered_df[col_name]

    metric_dict = {
        'current': todaydf[col_name].iloc[0],
        'metricmean': filtered_metric.mean(),
        'metricmin': filtered_metric.min(),
        'metricmax': filtered_metric.max(),
    }
    metric_dict['difference'] = metric_dict['current'] - metric_dict['metricmean']
    return metric_dict


def message_generator(activity_type, **kwargs):
    if 'work_commute' == activity_type:
        msg_dict = {
            'wow': 'Woah!',
            'activity': 'got to work',
            'support': 'Good Job',
            'metric': 'Commute Time:',
            'unit': 'mins'
        }
    elif 'home_commute' == activity_type:
        msg_dict = {
            'wow': 'Cool!',
            'activity': 'got home',
            'support': 'Great',
            'metric': 'Commute Time:',
            'unit': 'mins'
        }
    elif 'hours_at_work' == activity_type:
        msg_dict = {
            'wow': 'Woah!',
            'activity': 'left work',
            'support': 'Super',
            'metric': 'Hours at Work:',
            'unit': 'hrs'
        }
    else:
        msg_dict = {
            'wow': 'Huh!',
            'activity': 'not sure what you did',
            'support': 'Still ok though',
            'metric': '?:',
            'unit': '?s'
        }
    msg_dict['minmetric'] = 'Min:'
    msg_dict['avgmetric'] = '*Average:'
    msg_dict['maxmetric'] = 'Max:'
    msg_dict['diff'] = '*Difference:'
    for k, v in kwargs.items():
        msg_dict[k] = v


    msg = """
    {wow} You just {activity}! {support}! Here are your stats:
    {metric:<14} {current:>6.2f} {unit}
    {avgmetric:<14} {metricmean:>6.2f} {unit}
    -----------------------------------
    {diff:<14} {difference:>+6.2f} {unit}
    -----------------------------------
    More Info:
    {minmetric:<14} {metricmin:>6.2f} {unit}
    {maxmetric:<14} {metricmax:>6.2f} {unit}
    """.format(**msg_dict)
    return msg


ymdfmt = '%Y-%m-%d %H:%M:%S'
p = Paths()

logg = Log('commute.calculator', p.log_dir, 'commute', log_lvl="DEBUG")
logg.debug('Log initiated')

client_secret_path = p.google_client_secret
pb = PBullet(p.key_dict['pushbullet_api'])

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
# Force ISO date format -- sometimes Google sheets cell will leave out leading '0's
last_update = pd.datetime.strptime(processed_sheet.cell(1, 2).value, ymdfmt).strftime(ymdfmt)

commute_df = pd.DataFrame(sheet.get_all_records())

# Begin processing columns
# First, Date columns
commute_df['timestamp'] = pd.to_datetime(commute_df['Raw_date'], format='%B %d, %Y at %I:%M%p')
last_entry = max(commute_df['timestamp']).strftime(ymdfmt)

if last_update < last_entry:
    logg.debug('New log found.')
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
        #row = daily_commute_df.iloc[i]
        if int(daily_commute_df.loc[i, 'dow']) < 6:
            # work day
            df = commute_df[commute_df['date'] == daily_commute_df.loc[i, 'date']]
            time_left_home = grab_timestamp(df, 'left', 'HOME', '07:35')
            time_arrived_work = grab_timestamp(df, 'arrived', 'BAO_WORK', '08:25')
            time_left_work = grab_timestamp(df, 'left', 'BAO_WORK', '16:45')
            time_arrived_home = grab_timestamp(df, 'arrived', 'HOME', '17:30')
            # Calculate minutes for work commute
            daily_commute_df.loc[i, 'work_commute'] = pd.Timedelta(time_arrived_work['tstamp'] - time_left_home['tstamp']).seconds / 60
            daily_commute_df.loc[i, 'adjusted_work_commute'] = any([time_left_home['adjusted'], time_arrived_work['adjusted']])
            daily_commute_df.loc[i, 'hours_at_work'] = pd.Timedelta(time_left_work['tstamp'] - time_arrived_work['tstamp']).seconds / 60 / 60
            daily_commute_df.loc[i, 'home_commute'] = pd.Timedelta(time_arrived_home['tstamp'] - time_left_work['tstamp']).seconds / 60
            daily_commute_df.loc[i, 'adjusted_home_commute'] = any([time_left_work['adjusted'], time_arrived_home['adjusted']])

    # Save csv file
    logg.debug('Writing to csv.')
    daily_commute_df.to_csv(csv_save_path)

    # Loop through daily_commute_df and add to processed sheet on Google Sheets
    # Column title
    # processed_sheet.insert_row(daily_commute_df.columns.tolist(), index=1)
    # for i in range(daily_commute_df.shape[0]):
    #     row = daily_commute_df.iloc[i]
    #     row['date'] = row['date'].strftime('%Y-%m-%d')
    #     processed_sheet.insert_row(row.tolist(), index=i + 2)

    # Notify of my recent commute time
    latest_entry = commute_df[commute_df['timestamp'] == max(commute_df['timestamp'])].iloc[0]
    today_df = daily_commute_df[daily_commute_df['date'] == now.date()]
    msg = ''

    if latest_entry['activity'] == 'arrived' and latest_entry['Location'] == 'BAO_WORK':
        # Just arrived at work, analyze commute times
        # Generate message
        msg = message_generator('work_commute', **get_metrics(daily_commute_df, today_df, 'work_commute', False))
    elif latest_entry['activity'] == 'left' and latest_entry['Location'] == 'BAO_WORK':
        # Just arrived at work, analyze commute times
        # Generate message
        msg = message_generator('hours_at_work', **get_metrics(daily_commute_df, today_df, 'hours_at_work', False))
    elif latest_entry['activity'] == 'arrived' and latest_entry['Location'] == 'HOME':
        # Just arrived at work, analyze commute times
        # Generate message
        msg = message_generator('home_commute', **get_metrics(daily_commute_df, today_df, 'home_commute', False))

    if msg != '':
        logg.debug('Sending notification')
        pb.send_message('Commute Notification', msg)

    # Update cell with timestamp
    processed_sheet.update_cell(1, 2, pd.datetime.now().strftime(ymdfmt))

logg.close()