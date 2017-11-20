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
from logger.pylogger import Log
from primary.maintools import Paths
from primary.texttools import MarkovText, TextCleaner
from comm.commtools import Twitter


p = Paths()
logg = Log('twitkov.txtprocess', p.log_dir, 'twitkov')
logg.debug('Logging initiated')

tweepy_dict = eval(p.key_dict['tweepy_api'])
tw = Twitter(tweepy_dict)
tc = TextCleaner()

char_limit = 280
# Read in text sources
markov_dir = os.path.join(p.data_dir, 'markov')

fpaths = [os.path.join(markov_dir, x) for x in os.listdir(markov_dir)]

txt = {}
for f in fpaths:
    k = os.path.basename(f).replace('.txt', '')
    with open(f, 'r') as f:
        txt[k] = f.read()

choose_txt = [
    txt['debian'],
    txt['drawing'],
    txt['cooking2'],
    txt['conspiracy_list'] + txt['ajones1'],
    txt['compsci_workshops'],
    txt['romance1'],
]

mk = MarkovText(choose_txt, limit=30000)

sentences = mk.generate_n_sentences(50, char_limit)

sentence = sentences[randint(0, len(sentences) - 1)]
sentence = tc.sentence_filler(sentence, char_limit)

tw.post(sentence)

logg.close()
