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
import obd
from datetime import datetime as dt
import time
from collections import OrderedDict
from primary.maintools import CSVHelper, Paths
from logger.pylogger import Log


def is_engine_on(conn):
    try:
        response = conn.query(obd.commands.RPM)
        rval = response.value.magnitude
    except:
        rval = 0

    if rval is None:
        rval = 0

    if rval > 0:
        return True
    return False

chelp = CSVHelper()
p = Paths()
logg = Log('honda.obd', p.log_dir, 'obd_logger', log_lvl="DEBUG")
logg.debug('Logging initiated')
connection = obd.OBD()

save_path = os.path.join(p.data_dir, 'obd_results_{}.csv'.format(dt.now().strftime('%Y%m%d_%H%M%S')))

cmd_list = [
    'RUN_TIME',
    'RPM',
    'SPEED',
    'FUEL_LEVEL',
    'FUEL_RATE',
    'OIL_TEMP',
    'ENGINE_LOAD',
    'SHORT_FUEL_TRIM_1',
    'LONG_FUEL_TRIM_1',
    'DISTANCE_W_MIL',
    'FUEL_RAIL_PRESSURE_VAC',
    'FUEL_RAIL_PRESSURE_DIRECT',
    'FUEL_RAIL_PRESSURE_ABS',
    'INTAKE_PRESSURE',
    'TIMING_ADVANCE',
    'FUEL_INJECT_TIMING',
    'INTAKE_TEMP',
    'AMBIANT_AIR_TEMP',
    'MAF',
    'THROTTLE_POS',
    'AIR_STATUS',
    'BAROMETRIC_PRESSURE',
    'EVAPORATIVE_PURGE',
    'EVAP_VAPOR_PRESSURE',
    'O2_B1S1',
    'O2_B1S2',
    'O2_B1S3',
    'O2_B1S4',
    'O2_B2S1',
    'O2_B2S2',
    'O2_B2S3',
    'O2_B2S4',
    'CONTROL_MODULE_VOLTAGE',
    'ABSOLUTE_LOAD',
    'COMMANDED_EQUIV_RATIO',
    'RELATIVE_THROTTLE_POS',
    'THROTTLE_POS_B',
    'THROTTLE_POS_C',
    'RELATIVE_ACCEL_POS',
    'ACCELERATOR_POS_D',
    'ACCELERATOR_POS_E',
    'ACCELERATOR_POS_F',
    'THROTTLE_ACTUATOR',
    'RUN_TIME_MIL',
    'FUEL_TYPE',
    'ETHANOL_PERCENT',
]

result_dicts = []
t = time.time()
end_time = t + 60 * 5   # Run for five minutes
if is_engine_on(connection):
    # If engine is on, being recording...

    while is_engine_on(connection) and t < end_time:
        print('Beginning new line...')
        line_dict = OrderedDict(())
        line_dict['TIMESTAMP'] = dt.now().isoformat()
        for d in cmd_list:
            print('Working on {}.'.format(d))
            try:
                response = connection.query(obd.commands[d])
                rval = response.value.magnitude
            except:
                rval = None
                pass

            if rval is None:
                rval = 0

            # Append to dictionary
            line_dict[d] = rval

        # Append line of data to main dictionary
        result_dicts.append(line_dict)
        # Wait a second before continuing
        logg.debug('Results written to dict... Waiting...')
        time.sleep(1)
        t = time.time()

    logg.debug('Loop ended. Writing file.')
    # Save file
    chelp.ordered_dict_to_csv(result_dicts, save_path)

