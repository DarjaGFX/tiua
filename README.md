# TUIA

## Graph Dataset : http://an.kaist.ac.kr/~haewoon/release/twitter_social_graph/twitter_rv.zip
(webpage: http://an.kaist.ac.kr/traces/WWW2010.html)

## Tweets Dataset:
{
    https://ia800302.us.archive.org/5/items/archiveteam-twitter-stream-2012-01/archiveteam-twitter-2012-01.tar,
    https://ia800302.us.archive.org/5/items/archiveteam-twitter-stream-2012-01/archiveteam-twitter-2012-02.tar
}
(   
    wepage:{
        https://archive.org/details/archiveteam-twitter-stream-2012-01,
        https://archive.org/details/archiveteam-twitter-stream-2012-02
    }
)

"""
*id2json => reads users graph (twitter_rv.net) and makes "uson" with following format:
            {"Id" : {},"screen_name" : "","followers" : {}}


*insert_user_json => inserts "uson" to database.

*loadBaseUsers => reads users graph (twitter_rv.net) and writes unique ids in "base_ids.npy".

*seedTweets_mongoengine => searches for tweets in given directories, adds tweets and tweet's publisher user to database if user id is in "base_ids.npy" and user speaks ENGLISH!
"""

1 - Modify Settings.py (PATH and DIRECTORIES)
    {
        ### Database Name
        DBNAME = 'tiua'

        ROOT_DIRECTORIES = [
                    '/path/to/root/folder/of/extracted/tweetdataset1',
                    '/path/to/root/folder/of/extracted/tweetdataset2',
                    .
                    .
                    .
                ]

        #this file'll be created by loadBaseUsers.py
        BASE_IDS_PATH = 'path/to/base_ids.npy'

        #this file'll be created by seedTweets_mongoengine.py
        EXISTING_IDS_PATH = './indb_ids'

        GRAPH_PATH = "/path/to/user/graphs/dataset/twitter_rv.net"
    }

2 - Run loadBaseUsers.py

3 - Run seedTweets_mongoengine.py
