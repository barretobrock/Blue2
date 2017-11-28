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

list_of_keys = list(txt.keys())
# Randomly choose two sources
src1 = randint(0, len(list_of_keys))
src2 = randint(0, len(list_of_keys))
if src1 == src2:
    if src1 == 0:
        src1 += 1
    else:
        src1 -= 1

choose_txt = [
    txt[list_of_keys[src1]],
    txt[list_of_keys[src2]]
]


# This seems to break sometimes, so perform a loop of up to five times
for x in range(0, 5):
    try:
        mk = MarkovText(choose_txt, limit=5000)
        break
    except:
        pass


sentences = mk.generate_n_sentences(50, char_limit)

sentence = sentences[randint(0, len(sentences) - 1)]
sentence = tc.sentence_filler(sentence, char_limit)

tw.post(sentence, char_limit=char_limit)

logg.close()
