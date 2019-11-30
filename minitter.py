from mongoengine import *

class User(Document):
    Id             = IntField(unique = True, required = True)
    screen_name    = StringField(unique = True, required = True)

    def tweets(self, start, interval):
        """
        interval should be in miliseconds.
        """
        return tweet.objects(Q(Id = self.Id) & Q(timestamp__gte=start) & Q(timestamp__lte=start+interval))

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

class follows(Document):
    followee    =   ReferenceField(User, required=True)
    follower    =   ReferenceField(User, required=True)

class feedback(Document):
    """
    `actype` is True if `react` is a retweet of `target`, and False if it is a reply!
    """
    target  =   ReferenceField(tweet,required=True)
    react   =   ReferenceField(tweet,required=True)
    actype  =   BooleanField(required=True)
