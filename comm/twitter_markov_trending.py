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
import tweepy
from random import randint
from logger.pylogger import Log
from primary.maintools import Paths
from primary.texttools import MarkovText, TextCleaner
from comm.commtools import Twitter


p = Paths()
logg = Log('twitkov.trending', p.log_dir, 'twitkov')
logg.debug('Logging initiated')
tweepy_dict = eval(p.key_dict['tweepy_api'])
tw = Twitter(tweepy_dict)
tc = TextCleaner()

char_limit = 280

# Get current trending info for US
trends = tw.trends_place(23424977)[0]['trends']
# Randomly pick a trend in top 20
if len(trends) > 50:
    trend = trends[randint(0, 50)]
else:
    trend = trends[randint(0, len(trends))]

# Gather tweets with given hashtag
n_tweets = 2000
tweets = tweepy.Cursor(tw.search, q=trend['name']).items(n_tweets)

txt_list = []
for t in range(n_tweets):
    try:
        txt_list.append(tweets.next().text)
    except:
        pass
txt = ' '.join(txt_list)

# Create Markov model from tweets
mk = MarkovText(txt)
post_list = mk.generate_n_sentences(10, char_limit)

post_txt = post_list[randint(0, len(post_list) - 1)]
# Add trending hashtag
if len(post_txt + trend['name']) < char_limit:
    post_txt = ' '.join([post_txt, trend['name']])

post_txt = tc.sentence_filler(post_txt, char_limit)
tw.post(post_txt, char_limit=char_limit)
