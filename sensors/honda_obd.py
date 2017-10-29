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
import obd
from datetime import datetime as dt
import time
from collections import OrderedDict
from primary.maintools import CSVHelper, Paths
from logger.pylogger import Log


def is_engine_on(conn):
    """Determines if engine is running"""
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


mesurement_interval = 1 # time to wait between measurements
p = Paths()
logg = Log('honda.obd', p.log_dir, 'obd_logger', log_lvl="DEBUG")
logg.debug('Logging initiated')
chelp = CSVHelper()
# Set path to write file to
save_path = os.path.join(p.data_dir, 'obd_results_{}.csv'.format(dt.now().strftime('%Y%m%d_%H%M%S')))

# Get commands
cmd_list = [x.name for x in obd.commands[1][4:]]

result_dicts = []
t = time.time()
end_time = t + 60 * 5   # Run for five minutes
end_time -= 5   # Take off five seconds for processing

connection = obd.OBD()
while time.time() < end_time:
    if not connection.is_connected():
        # Make sure bluetooth is connected. Otherwise try connecting to it
        # Attempt to make connection.
        connection = obd.OBD()
        if not connection.is_connected():
            # Sleep if still no success
            time.sleep(mesurement_interval)
    else:
        if is_engine_on(connection):
            # If engine is on, being recording...
            while is_engine_on(connection) and time.time() < end_time:
                line_dict = OrderedDict(())
                line_dict['TIMESTAMP'] = dt.now().isoformat()
                for d in cmd_list:
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
                time.sleep(mesurement_interval)

            logg.debug('Loop ended. Writing file.')
            # Save file
            chelp.ordered_dict_to_csv(result_dicts, save_path)
        else:
            time.sleep(mesurement_interval)

logg.close()
