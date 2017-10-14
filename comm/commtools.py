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
from pushbullet import PushBullet
import time
import datetime
import os
import codecs


class DomoticzComm:
    def __init__(self, server, port=8080):
        self.server = server
        self.port = port
        self.prefix_url = 'http://{}:{}/json.htm?type=command'.format(self.server, self.port)
        self.curl_type = 'Accept: application/json'

    def switch_on(self, device_id):
        url = '{}&param=switchlight&idx={}&switchcmd=On'.format(self.prefix_url, device_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def switch_off(self, device_id):
        url = '{}&param=switchlight&idx={}&switchcmd=Off'.format(self.prefix_url, device_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def toggle_switch(self, device_id):
        url = '{}&param=switchlight&idx={}&switchcmd=Toggle'.format(self.prefix_url, device_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def send_sensor_data(self, device_id, value):
        url = '{}&param=udevice&idx={}&nvalue=0&svalue={}'.format(self.prefix_url, device_id, value)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def switch_group_off(self, group_id):
        url = '{}&param=switchscene&idx={}&switchcmd=Off'.format(self.prefix_url, group_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])

    def switch_group_on(self, group_id):
        url = '{}&param=switchscene&idx={}&switchcmd=On'.format(self.prefix_url, group_id)
        subprocess.check_call(['curl', '-s', '-i', '-H', self.curl_type, url])


class Email:
    """
    Prepares and sends email to desired recipient(s)
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


class PBullet:
    def __init__(self, api):
        self.api = api
        self.pb = PushBullet(self.api)

    def send_message(self, title, message):
        # Send Pushbullet text notification
        self.pb.push_note(title, message)

    def send_address(self, title, address):
        # Send address
        self.pb.push_address(title, address)

    def send_link(self, text, link):
        # Send link
        self.pb.push_link(text, link)

    def send_img(self, filepath, title, filetype='image/png'):
        with open(filepath, 'rb') as thing:
            file_data = self.pb.upload_file(thing, title, file_type=filetype)
        push = self.pb.push_file(**file_data)


class Camera:
    def __init__(self):
        pass

    def capture_image(self, save_dir, res=(1280, 720), framerate=24, extra_text='', timestamp=True, vflip=False, hflip=False):
        from picamera import PiCamera
        # Captue image and return path of where it is saved
        filename = '{}.png'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        save_path = os.path.join(save_dir, filename)
        camera = PiCamera()
        camera.resolution = res
        camera.framerate = framerate
        cam_text = ''
        camera.vflip = vflip
        camera.hflip = hflip

        if timestamp:
            cam_text = '{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if extra_text is not '':
            cam_text = '{}-{}'.format(extra_text, cam_text)
        camera.annotate_text = cam_text
        camera.capture(save_path)
        return save_path


