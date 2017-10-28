#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from picamera import PiCamera

class Camera:
    def __init__(self):

        pass

    def capture_image(self, save_dir, res=(1280, 720), framerate=24, extra_text='', timestamp=True, vflip=False, hflip=False):
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

