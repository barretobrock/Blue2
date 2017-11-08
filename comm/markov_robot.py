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
    sys.path.insert(0, os.path.join(cur_dir, 'blue2'))
# import custom modules
from random import randint
from primary.maintools import Paths
from primary.texttools import MarkovText, WebExtractor, TextCleaner
from comm.commtools import Twitter


p = Paths()
tweepy_dict = eval(p.key_dict['tweepy_api'])
tw = Twitter(tweepy_dict)
webex = WebExtractor()
tcln = TextCleaner()

char_limit = 140
# Read in text sources
markov_dir = os.path.join(p.data_dir, 'markov')

# Extract text from link
#txt_list = webex.get_text('https://www.infowars.com/transcript-alex-jones-secede-from-the-new-world-order/')
#txt = ' '.join([x.text for x in txt_list])

#with open(os.path.join(markov_dir, 'ajones1.txt'), 'w') as f:
#    f.write(txt)

fpaths = [os.path.join(markov_dir, x) for x in os.listdir(markov_dir)]

txt = {}
for f in fpaths[:4]:
    k = os.path.basename(f).replace('.txt', '')
    with open(f, 'r') as f:
        txt[k] = f.read()

mk = MarkovText(txt, limit=5000)

sentences = mk.generate_n_sentences(50, char_limit)

sentence = sentences[randint(0, len(sentences) - 1)]

tw.update_status(sentence)