#!/usr/bin/env python3
"""
General tools used throughout a majority of scripts:
    * Absolute paths
    * Date procesing
    * CSV processing
    * Text processing
"""
import os
import socket
import csv
import datetime
from collections import OrderedDict
import base64


class Paths:
    def __init__(self):
        # locations
        self.home_loc = '30.457344,-97.655014'

        # ip addresses
        self.gatewaypi_ip = '192.168.0.5'
        # directories
        hostname = socket.gethostname()
        if any([name in hostname for name in ['MacBook', 'buntu']]):
            if 'MacBook' in hostname:
                self.home_dir = os.path.abspath('/Users/barret/')
            elif 'buntu' in hostname:
                self.home_dir = os.path.abspath('/home/barretobrock/')
            else:
                ValueError('Unknown hostname: {}'.format(hostname))
            self.home_dir = os.path.join(*[self.home_dir, 'Dropbox', 'Programming', 'Scripts'])
        else:
            self.home_dir = os.path.abspath('/home/pi')
        self.image_dir = os.path.join(self.home_dir, 'images')
        self.lpbot_dir = os.path.join(self.home_dir, 'LPBOT')
        self.data_dir = os.path.join(self.lpbot_dir, 'Data')
        self.script_dir = os.path.join(self.lpbot_dir, 'Scripts')
        self.log_dir = os.path.join(self.lpbot_dir, 'Logs')
        self.key_dir = os.path.join(self.home_dir, 'keys')
        # files
        self.dark_sky_api_path = os.path.join(self.key_dir, 'dark_sky_api.txt')
        self.pushbullet_api_path = os.path.join(self.key_dir, 'pushbullet_api.txt')
        # keys
        with open(self.dark_sky_api_path) as f1, open(self.pushbullet_api_path) as f2:
            self.dark_sky_api = f1.read().replace('\n', '')
            self.pushbullet_api = f2.read().replace('\n', '')


class DateTools:
    def __init__(self):
        pass

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def string_to_datetime(self, datestring, strftime_string='%Y%m%d'):
        return datetime.datetime.strptime(datestring, strftime_string)

    def string_to_unix(self, date_string, strftime_string='%Y%m%d'):
        unix = (datetime.datetime.strptime(date_string, strftime_string) - datetime.datetime(1970, 1, 1)).total_seconds()
        return unix * 1000

    def unix_to_string(self, unix_date, output_fmt='%Y-%m-%d'):
        date_string = datetime.datetime.fromtimestamp(unix_date).strftime(output_fmt)
        return date_string


class CSVHelper:
    def __init__(self, delimiter=';', lineterminator='\n'):
        self.delimiter = delimiter
        self.lineterminator = lineterminator

    def csv_to_ordered_dict(self, path_to_csv, encoding='UTF-8'):

        list_out = []
        with open(path_to_csv, 'r', encoding=encoding) as f:
            reader = csv.reader(f, delimiter=self.delimiter, lineterminator=self.lineterminator)
            keys = next(reader)
            for row in reader:
                list_out.append(OrderedDict(zip(keys, row)))
        return list_out

    def ordered_dict_to_csv(self, data_dict, path_to_csv, writetype='w', encoding='UTF-8'):
        # saves list of list of ordered dicts to path
        # determine how deep to go: if list of lists, etc
        islistoflist = False
        if isinstance(data_dict[0], list):
            if isinstance(data_dict[0][0], OrderedDict):
                islistoflist = True

        with open(path_to_csv, writetype, encoding=encoding) as f:
            if islistoflist:
                keys = data_dict[0][0].keys()
            else:
                keys = data_dict[0].keys()
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore', delimiter=self.delimiter, lineterminator=self.lineterminator)
            # If appending, don't write a header string
            if writetype == 'w':
                writer.writeheader()
            # Write data to file based on depth
            if islistoflist:
                for row in data_dict:
                    writer.writerows(row)
            else:
                writer.writerows(data_dict)

    def txt_to_list(self, path_to_txt, delimiter):
        '''
        Convert text with characters serving as delimiter to list
        :param path_to_txt: absolute file path to text file
        :param delimiter: delimiter character
        :return:
        '''
        with open(path_to_txt) as f:
            txtstr = f.read().split(delimiter)
            if ''.join(txtstr) == '':
                txtlist = []
            else:
                txtlist = list(map(int, txtstr[:len(txtstr)]))
        return txtlist


class TextHelper:
    def __init__(self):
        pass

    def mass_replace(self, find_strings, replace_strings, in_text):
        # Replace multiple strings at once
        for x in range(0, len(find_strings)):
            if isinstance(replace_strings, list):
                if len(replace_strings) != len(find_strings):
                    raise ValueError('Lists not the same size!')
                else:
                    in_text = in_text.replace(find_strings[x], replace_strings[x])
            else:
                in_text = in_text.replace(find_strings[x], replace_strings)
        return in_text