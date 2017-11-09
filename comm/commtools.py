#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A suite of communication tools
-email
-pushbullet
-more to come?
"""
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
from smtplib import SMTP
import socket
import os
from tweepy.api import API


class PBullet:
    """
    Connects to Pushbullet API
    Args for __init__:
        api: str, Pushbullet API key
    """
    def __init__(self, api):
        self.pushbullet = __import__('pushbullet')

        self.api = api
        self.pb = self.pushbullet.PushBullet(self.api)

    def send_message(self, title, message):
        """Sends a message"""
        self.pb.push_note(title, message)

    def send_address(self, title, address):
        """Sends an address"""
        self.pb.push_address(title, address)

    def send_link(self, text, link):
        """Sends a link"""
        self.pb.push_link(text, link)

    def send_img(self, filepath, title, filetype='image/png'):
        """Sends an image"""
        with open(filepath, 'rb') as thing:
            file_data = self.pb.upload_file(thing, title, file_type=filetype)
        push = self.pb.push_file(**file_data)


class Inet:
    """
    Performs variety of internet connection tests
    """
    def __init__(self):
        pass

    def get_ip_address(self):
        """Retrieves the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        except:
            return ''

    def ping_success(self, is_internal=False):
        """
        Checks if connected to internet
        Args:
            is_internal: boolean, pings internal network if True. default False
        """
        if is_internal:
            host = "192.168.0.1"
        else:
            host = "8.8.8.8"
        response = os.system("ping -c 1 {}".format(host))
        if response == 0:
            return True
        else:
            return False


class Email:
    """
    Prepares and sends email to desired recipient(s)
    Args from __init__:
        email_from: str, user's email address
        pw: str, password for user's email address
        email_to: list of strings, email address(es) to which a message will be sent
        subject: str, subject of message
        body: str, body of message
        log: Logger-type class object for following email dispatch status
        attachment_paths: list of paths to attach to email. default = empty
    """
    def __init__(self, email_from, pw, email_to, subject, body, log, attachment_paths=[]):
        self.email_from = email_from
        self.pw = pw
        self.email_to = email_to
        self.subject = subject
        self.body = body
        self.attachment_paths = attachment_paths
        self.log = log

    def send(self):
        """Command to package and send email"""
        self.log.debug('Beginning email process.')
        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["To"] = ', '.join([self.email_to])
        msg["Subject"] = self.subject
        msg.preamble = self.body
        if len(self.attachment_paths) > 0:
            self.log.debug('Encoding any attachments')
            for attachment_path in self.attachment_paths:
                ctype, encoding = mimetypes.guess_type(attachment_path)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)
                if maintype == 'text':
                    with open(attachment_path) as f:
                        attachment = MIMEText(f.read(), _subtype=subtype)
                else:
                    with open(attachment_path) as f:
                        attachment = MIMEBase(maintype, subtype)
                        attachment.set_payload(f.read())
                        encoders.encode_base64(attachment)
                attachment.add_header("Content-Disposition", 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(attachment)
        self.log.debug('Communicating with server.')
        try:
            server = SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.email_from, self.pw)
            self.log.debug('Connected with email server.')
            server.sendmail(self.email_from, self.email_to, msg.as_string())
            self.log.debug('Message sent.')
            server.quit()
        except TimeoutError:
            self.log.exception('Connection with server timed out.')
        except:
            self.log.exception('Could not connect with email server.')


class DomoticzComm:
    """
    Send and receive data from a computer running Domoticz Home Automation server
    Args for __init__:
        server: local IP of server running Domoticz master
        port: Domoticz connection port. default=8080
    """
    def __init__(self, server, port=8080):
        self.server = server
        self.port = port
        self.prefix_url = 'http://{}:{}/json.htm?type=command'.format(self.server, self.port)
        self.curl_type = 'Accept: application/json'

    def switch_on(self, device_id):
        """Sends an 'on' command to a given switch's id"""
        url = '{}&param=switchlight&idx={}&switchcmd=On'.format(self.prefix_url, device_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def switch_off(self, device_id):
        """Sends an 'off' command to a given switch's id"""
        url = '{}&param=switchlight&idx={}&switchcmd=Off'.format(self.prefix_url, device_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def toggle_switch(self, device_id):
        """Toggle a given switch between 'on' and 'off'"""
        url = '{}&param=switchlight&idx={}&switchcmd=Toggle'.format(self.prefix_url, device_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def send_sensor_data(self, device_id, value):
        """
        Send data collected from a certain sensor
        Args:
            device_id: int, id of the given device
            value: float, measurement made by the given sensor
        """
        url = '{}&param=udevice&idx={}&nvalue=0&svalue={}'.format(self.prefix_url, device_id, value)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def switch_group_off(self, group_id):
        """Switches off a group based on its id"""
        url = '{}&param=switchscene&idx={}&switchcmd=Off'.format(self.prefix_url, group_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def switch_group_on(self, group_id):
        """Switches on a group based on its id"""
        url = '{}&param=switchscene&idx={}&switchcmd=On'.format(self.prefix_url, group_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])


class Twitter(API):
    def __init__(self, key_dict):
        self.twp = __import__('tweepy')
        # Import keys
        self.CONSUMER_KEY = key_dict['consumer_key']
        self.CONSUMER_SECRET = key_dict['consumer_secret']
        self.ACCESS_KEY = key_dict['access_key']
        self.ACCESS_SECRET = key_dict['access_secret']
        auth = self.twp.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        super(Twitter, self).__init__(auth)

    def get_messages(self):
        msgs = self.direct_messages()
        return msgs

    def get_followers(self):
        followers = self.followers()
        return followers

    def post(self, text, log=None, char_limit=140):
        if text != "":
            if len(text) > char_limit:
                text = text[:char_limit]
            try:
                self.update_status(status=text)
            except:
                if log is not None:
                    log.exception('Failed to post tweet.')
                else:
                    raise ValueError('Tweet failed to post!')
                    pass

    def send_message(self, user_id, text):
        if text != "":
            self.send_direct_message(user_id=user_id, text=text)

    def delete_tweet(self, datetime_lim, containing=""):
        timeline = self.twp.Cursor(self.user_timeline).items()
        for tweet in timeline:
            if tweet.created_at < datetime_lim:
                if containing != "":
                    if containing in tweet.text:
                        print("Destroying {}\n{}".format(tweet.id, tweet.text))
                        self.destroy_status(tweet.id)
                else:
                    print("Destroying {}\n{}".format(tweet.id, tweet.text))
                    self.destroy_status(tweet.id)

