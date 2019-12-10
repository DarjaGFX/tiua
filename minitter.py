from mongoengine import *

class User(Document):
    Id             = IntField(unique = True, required = True)
    screen_name    = StringField(unique = True, required = True)

    def tweets(self, start= None, interval= None):
        """
        interval should be in miliseconds.
        """
        if start = None :
            return tweet.objects.filter(user = self)
        if interval = None :
            return tweet.objects.filter(Q(user = self) & Q(timestamp__gte=start))
        return tweet.objects.filter(Q(user = self) & Q(timestamp__gte=start) & Q(timestamp__lte=start+interval))

    def followers(self):
        return follows.objects.filter(followee= self)

class tweet(Document):
    Id         = IntField(unique = True , required = True)
    user       = ReferenceField(User)
    created_at = DateTimeField(required = True)
    timestamp  = FloatField(required = True)
    text       = StringField(required = True)
    is_reply   = BooleanField(required = True)
    is_quote   = BooleanField(required = True)
    is_retweet = BooleanField(required = True)
    entities   = DictField(ListField())

    def url(self):
        res = 'https://twitter.com/{}/status/{}'.format(self.user.screen_name, self.Id)
        return res

class follows(Document):
    followee    =   ReferenceField(User, required=True)
    follower    =   ReferenceField(User, required=True)

class feedback(Document):
    """
    `actype` is -1 if `react` is a Qoute, 0 if it's a retweet and 1 if it is a reply of `target`!
    """
    target  =   ReferenceField(tweet,required=True)
    react   =   ReferenceField(tweet,required=True)
    actype  =   IntField(required=True)
