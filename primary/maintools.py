#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General tools used throughout a majority of scripts:
    * Absolute paths
    * Date processing
    * CSV processing
    * Text processing
"""
import os
import socket
import csv
import datetime
from collections import OrderedDict
import glob


class Paths:
    def __init__(self):
        # locations
        self.home_loc = '30.457344,-97.655014'

        # ip addresses
        self.gatewaypi_ip = '192.168.0.5'
        self.server_ip = '192.168.0.3'
        self.webcam_ip = '192.168.0.7'
        self.server_hostname = 'bobrock'
        # directories
        hostname = socket.gethostname()
        self.home_dir = os.path.expanduser("~")
        if 'macbook' in hostname.lower():
            self.home_dir = os.path.join(*[self.home_dir, 'Dropbox', 'Programming', 'Scripts'])

        self.image_dir = os.path.join(self.home_dir, 'images')
        self.data_dir = os.path.join(self.home_dir, 'data')
        self.script_dir = os.path.join(self.home_dir, 'blue2')
        self.log_dir = os.path.join(self.home_dir, 'logs')
        self.key_dir = os.path.join(self.home_dir, 'keys')
        # filepaths
        self.privatekey_path = os.path.join(os.path.expanduser('~'), *['.ssh', 'id_rsa'])
        self.google_client_secret = os.path.join(self.key_dir, 'client_secret.json')
        self.ip_path = os.path.join(self.key_dir, 'myip.txt')

        # key filepaths
        file_list = [
            'darksky_api.txt',
            'pushbullet_api.txt',
            'plotly_api.txt',
            'tweepy_api.txt',
            'personal_tweepy_api.txt',
            'webcam_api.txt',
        ]

        self.key_dict = {}

        for tfile in file_list:
            fpath = os.path.join(self.key_dir, tfile)
            if os.path.isfile(fpath):
                with open(fpath) as f:
                    self.key_dict[tfile.replace('.txt', '')] = f.read().replace('\n', '')


class DateTools:
    def __init__(self):
        pass

    def last_day_of_month(self, any_day):
        """Retrieves the last day of the month for the given date"""
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def string_to_datetime(self, datestring, strftime_string='%Y%m%d'):
        """Converts string to datetime"""
        return datetime.datetime.strptime(datestring, strftime_string)

    def string_to_unix(self, date_string, strftime_string='%Y%m%d'):
        """Converts string to unix"""
        unix = (datetime.datetime.strptime(date_string, strftime_string) - datetime.datetime(1970, 1, 1)).total_seconds()
        return unix * 1000

    def unix_to_string(self, unix_date, output_fmt='%Y-%m-%d'):
        """Convert unix timestamp to string"""
        date_string = datetime.datetime.fromtimestamp(unix_date).strftime(output_fmt)
        return date_string

    def seconds_since_midnight(self, timestamp):
        """Calculates the number of seconds since midnight"""
        seconds = (timestamp - timestamp.replace(hour=0, minute=0, second=0)).total_seconds()
        return seconds


class FileSCP:
    """
    Establishes a connection for securely copying files from computer to computer.
    Args for __init__:
        privatekey_path: path to privatekey (in "~/.ssh/id_rsa")
        server_ip: Local ip address for home server computer
        server_hostname: Home server's hostname
    Note:
        privatekey has to be generated through this command:
            ssh-keygen -t rsa -C <USERNAME>@<HOSTNAME> OR
            ssh-keygen -t rsa -C "SOMETHING EASIER TO REMEMBER"
            Then press <Enter> 2x
            Then copy id_rsa.pub file to target computer
            cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP-ADDRESS> 'cat >> .ssh/authorized_keys'
    """
    def __init__(self, privatekey_path, server_ip, server_hostname):
        # Import paramiko
        self.pmiko = __import__('paramiko')

        mkey = self.pmiko.RSAKey.from_private_key_file(privatekey_path)

        self.ssh = self.pmiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(self.pmiko.AutoAddPolicy())
        # Connect to server using private key
        self.ssh.connect(server_ip, username=server_hostname, pkey=mkey)
        self.sftp = self.ssh.open_sftp()

    def scp_transfer(self, source_path, dest_path, is_remove_file=False):
        """
        Securely copy a file form source to destination
        Args:
            source_path: path of file to be copied
            dest_path: path to file's destination
            is_remove_file: bool, whether to remove the file from source after copy
                default: False
        """
        self.sftp.put(source_path, dest_path)
        if is_remove_file:
            # Try to remove file after successful transfer
            os.remove(source_path)


class CSVHelper:
    """
    Handles CSV <-> OrderedDictionary reading/writing.
    Args for __init__:
        delimiter: character that delimits the CSV file. default: ';'
        linetermination: character that signals a line termination. default: '\n'
    """
    def __init__(self, delimiter=';', lineterminator='\n'):
        self.delimiter = delimiter
        self.lineterminator = lineterminator

    def csv_to_ordered_dict(self, path_to_csv, encoding='UTF-8'):
        """
        Imports CSV file to list of OrderedDicts
        Args:
            path_to_csv: str, path to csv file
            encoding: type of encoding to read in the file.
                default: 'UTF-8'
        """
        list_out = []
        with open(path_to_csv, 'r', encoding=encoding) as f:
            reader = csv.reader(f, delimiter=self.delimiter, lineterminator=self.lineterminator)
            keys = next(reader)
            for row in reader:
                list_out.append(OrderedDict(zip(keys, row)))
        return list_out

    def csv_compacter(self, compacted_data_path, path_with_glob, sort_column='', remove_files=True):
        """
        Incorporates many like CSV files into one, with sorting for date column, if needed
        Args:
            compacted_data_path: path to file where compacted csv file will be saved.
                Doesn't have to exist
            path_with_glob: Full path where csv file group is taken. '*' is wildcard.
            sort_column: str, sorts combined data frame by given column name.
                Default = ''
            remove_files: bool, default = True
        """
        if os.path.exists(compacted_data_path):
            master_df = self.csv_to_ordered_dict(compacted_data_path)
        else:
            master_df = []

        list_of_files = glob.glob(path_with_glob)
        new_df_list = []
        if len(list_of_files) > 0:
            # Iterate through each file, combine
            for csvfile in list_of_files:
                df = self.csv_to_ordered_dict(csvfile)
                new_df_list += df
            master_df += new_df_list

            # Sort dataframe
            if sort_column != '':
                if sort_column.lower() in [x.lower() for x in master_df[0].keys()]:
                    # Determine the column to be sorted
                    for c in master_df[0].keys():
                        if c.lower() == sort_column.lower():
                            col = c
                            break
                    master_df = sorted(master_df, key=lambda k: k[col])
            # Save appended dataframe
            self.ordered_dict_to_csv(master_df, compacted_data_path)
            if remove_files:
                for csvfile in list_of_files:
                    os.remove(csvfile)

    def ordered_dict_to_csv(self, data_dict, path_to_csv, writetype='w'):
        """
        Exports given list of OrderedDicts to CSV
        Args:
            data_dict: OrderedDict or list of OrderedDicts to export
            path_to_csv: destination path to CSV file
            writetype: 'w' for writing or 'a' for appending
        """
        # saves list of list of ordered dicts to path
        # determine how deep to go: if list of lists, etc
        islistoflist = False
        if isinstance(data_dict[0], list):
            if isinstance(data_dict[0][0], OrderedDict):
                islistoflist = True

        with open(path_to_csv, writetype) as f:
            if islistoflist:
                keys = data_dict[0][0].keys()
            else:
                keys = data_dict[0].keys()
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore', delimiter=self.delimiter,
                                    lineterminator=self.lineterminator)
            # If appending, don't write a header string
            if writetype == 'w':
                writer.writeheader()
            # Write data to file based on depth
            if islistoflist:
                for row in data_dict:
                    writer.writerows(row)
            else:
                writer.writerows(data_dict)


class TextHelper:
    """
    Text manipulation tool for repetitive tasks
    """
    def __init__(self):
        pass

    def mass_replace(self, find_strings, replace_strings, in_text):
        """
        Performs multiple replace commands for lists of strings
        Args:
            find_strings: list of strings to find
            replace_strings: list of strings to replace find_strings with
            in_text: string to perform replacements
        Note:
            1.) len(replace_strings) == len(find_strings) OR
            2.) len(find_strings) > 1 and len(replace_strings) == 1
        """
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

    def txt_to_list(self, path_to_txt, delimiter):
        """Convert txt in file to list with provided character serving as delimiter"""
        with open(path_to_txt) as f:
            txtstr = f.read().split(delimiter)
            if ''.join(txtstr) == '':
                txtlist = []
            else:
                txtlist = list(map(int, txtstr[:len(txtstr)]))
        return txtlist
