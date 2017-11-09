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
logg = Log('twitkov.userhist', p.log_dir, 'twitkov')
logg.debug('Logging initiated')
tweepy_dict = eval(p.key_dict['tweepy_api'])
tw = Twitter(tweepy_dict)
tc = TextCleaner()

char_limit = 140
markov_dir = os.path.join(p.data_dir, 'markov')
# Get user id for user
users = tw.lookup_users(screen_names=['realDonaldTrump'])
user_id = users[0].id

alltweets = []
new_tweets = tw.user_timeline(user_id=user_id, count=200)
alltweets += new_tweets
oldest = alltweets[-1].id - 1

while len(new_tweets) > 0:
    new_tweets = tw.user_timeline(user_id=user_id, count=200, max_id=oldest)
    alltweets += new_tweets
    oldest = alltweets[-1].id - 1

txt_list = []
for tweet in alltweets:
    txt_list.append(tweet.text)
txt = ' '.join(txt_list)

with open(os.path.join(markov_dir, 'cooking1.txt')) as f:
    cooktxt = f.read()

txt = [txt, cooktxt]

with open(os.path.join(markov_dir, 'trumptweets.txt'), 'w') as f:
    f.write(txt)

# Create Markov model from tweets
mk = MarkovText(txt)
post_list = mk.generate_n_sentences(10, char_limit)

post_txt = post_list[randint(0, len(post_list) - 1)]
# Add trending hashtag
if len(post_txt + trend['name']) < char_limit:
    post_txt = ' '.join([post_txt, trend['name']])

post_txt = tc.sentence_filler(post_txt, char_limit)
tw.post(post_txt)
