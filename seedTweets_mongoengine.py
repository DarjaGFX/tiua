import re
import os
import bz2
from mongoengine import *
import json
import pandas as pd
import minitter as mt
import numpy as np
from Settings import *
import timer

connect(DBNAME)

print('loading base user ids')
bids = set(np.ndarray.tolist(np.load(BASE_IDS_PATH)))
print('base user ids loaded.')
print('seeding Mongodb...')

QOUTE = -1
RETWEET = 0
REPLY = 1

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
                    ### USER
                    try:
                        u1 = mt.User.objects.filter(Id = int(tweet_json['user']['id']) ).get()
                    except:
                        u1 = mt.User(
                            Id          = int(tweet_json['user']['id']),
                            screen_name = tweet_json['user']['screen_name']
                        )
                        u1.save()
                        r = open(EXISTING_IDS_PATH, 'a')
                        r.write('{}\n'.format(u1.Id))
                        r.close()
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
                    is_quote    = re.match(r'.+ RT @\w+: .+',tweet_json['text']) != None,
                    is_retweet  = 'retweeted_status' in tweet_json,
                    entities    = tweet_json['entities']
                )
                twt.save()

                ### feedback
                ###### ReTweet
                if 'retweeted_status' in tweet_json:
                    react = twt
                    target = mt.tweet.objects.filter(Id= int(tweet_json['retweeted_status']['id'])).get()
                    mt.feedback(
                    target= target,
                    react= react,
                    actype= RETWEET
                    ).save()
                ###### Qoute
                elif twt.is_quote:
                    react = twt
                    sn_pattern = r'.+ RT @(\w+): .+'
                    sn = re.findall(sn_pattern,twt.text)
                    sn = sn[0]
                    tt_pattern = r'.+ RT @\w+: (.+)'
                    tweet_text = re.findall(tt_pattern,twt.text)
                    tweet_text = tweet_text[0]
                    user = mt.User.objects.filter(screen_name= sn).get()
                    target = mt.tweet.objects.filter(Q(user= user) & Q(text= tweet_text)).get()
                    mt.feedback(
                    target= target,
                    react= react,
                    actype= QOUTE
                    ).save()
                ###### Reply
                if twt.is_reply:
                    react = twt
                    target = mt.tweet.objects.filter(Id= int(tweet_json['in_reply_to_status_id'])).get()
                    mt.feedback(
                        target= target,
                        react= react,
                        actype= REPLY
                    ).save()
            except:
                pass

timer.start()

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
        print('{}/{} \t|\tadding {} of {}\t | \t {} %\t | \t {}% of total. {}'.format(
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

timer.end()
timer.printlog()
