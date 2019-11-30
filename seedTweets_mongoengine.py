from datetime import datetime
import re
import os
import bz2
from mongoengine import *
import json
import pandas as pd
import minitter as mt
import numpy as np
from Settings import *

connect(DBNAME)

print('loading base user ids')
bids = set(np.ndarray.tolist(np.load(BASE_IDS_PATH)))
print('base user ids loaded.')
print('seeding Mongodb...')


def add_user_tweet(list_of_jsons):
    """
    gets list of jsons, tries to load jsons, and get/create users and tweets
    """
    for i in list_of_jsons:
            try:
                tweet_json = json.loads(i)
            except:
                continue
            if 'delete' in tweet_json:
                continue
            try:
                if int(tweet_json['user']['id']) in bids and tweet_json['user']['lang']== 'en':
                    r = open(EXISTING_IDS_PATH, 'a')
                    r.write('{}\n'.format(int(tweet_json['user']['id'])))
                    r.close()
                    ### USER
                    try:
                        u1 = mt.User.objects.filter(Id = int(tweet_json['user']['id']) ).get()
                    except:
                        u1 = mt.User(
                            Id          = int(tweet_json['user']['id']),
                            screen_name = tweet_json['user']['screen_name']
                        )
                        u1.save()
                else:
                    continue
            except:
                continue

            try:
                ### tweet
                twt = mt.tweet(
                    Id          = tweet_json['id'],
                    user        = u1,
                    created_at  = tweet_json['created_at'],
                    timestamp   = pd.to_datetime(tweet_json['created_at']).timestamp(),
                    text        = tweet_json['text'],
                    is_reply    = tweet_json['in_reply_to_status_id']!=None,
                    is_quote    = re.match(r'.+ RT .+',tweet_json['text']) != None,
                    is_retweet  = re.match(r'^RT .+',tweet_json['text']) != None,
                    entities    = tweet_json['entities']
                )
                twt.save()
                ### feedback
                if tweet_json['in_reply_to_status_id']!=None:
                    react = twt
                    target = mt.tweet.objects.filter(Id= int(tweet_json['in_reply_to_status_id'])).get()
                    mt.feedback(
                        target= target,
                        react= react,
                        actype= False
                    ).save()
                if e.match(r'^RT .+',tweet_json['text']) != None:
                    react = twt
                    target = mt.tweet.objects.filter(Id= int(tweet_json['retweeted_status']['id'])).get()
                    mt.feedback(
                        target= target,
                        react= react,
                        actype= True
                    ).save()
            except:
                pass

print(datetime.utcnow())

__ = 1
total = 0
for path in ROOT_DIRECTORIES:
    tree = [x[0]+'/'+tfile for x in os.walk(path) for tfile in x[2] if '.bz2' in tfile ]
    _ = 1
    total += len(tree)
    for full_name in tree:
        b = bz2.decompress(open(full_name,'rb').read())
        b = b.decode()
        b = b.split('\n')
        print('{}/{} \t|\t-adding {} of {}\t | \t {} %\t | \t {}% of total. {}'.format(
                __,
                len(ROOT_DIRECTORIES),
                _,
                len(tree),
                _*100//len(tree),
                (total-len(tree)+_)*100/total, ' '*20
            ),
            end='\r'
        )
        _ += 1
        add_user_tweet(b)
    __ += 1
print('Done.')

print(datetime.utcnow())
