from mongoengine import *
from Settings import DBNAME
import minitter as mt
import timer
import ModifiedLSH as mlsh
import StopWords as sw

connect(DBNAME)


def triplet(tweet):
    if tweet:
        reps = set()
        for r in mt.feedback.objects.filter(Q(target=tweet) & Q(actype=1)):
            reps.add(r.react.user)
        rets = set()
        for r in mt.feedback.objects.filter(Q(target=tweet) & Q(actype=0)):
            rets.add(r.react.user)
        qoutes = set()
        for r in mt.feedback.objects.filter(Q(target=tweet) & Q(actype=-1)):
            qoutes.add(r.react.user)

        repsCount = 0
        for i in reps:
            repsCount += len(i.followers())

        retsCount = 0
        for i in rets:
            retsCount += len(i.followers())

        qoutesCount = 0
        for i in qoutes:
            qoutesCount += len(i.followers())

        mt.TInfluence(
            tweet = tweet,
            sf_reply = repsCount,
            sf_retweet = retsCount,
            sf_qoute = qoutesCount,
            sf_similarities = 0
        ).save()


def preprocess(text):
    text = text.replace('.', ' ').replace(',', ' ').replace(':', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')

    if "RT @" in text.upper():
        text = text.upper().replace("RT ", '')
    set = text.split()
    for i in sw.SW:
        if i in set and i != ' ':
            set.remove(i)
    return " ".join(set)


def similarity(t1, t2):
    unin = set()
    unin.update(t1)
    unin.update(t2)
    s1 = []
    s2 = []
    for i in unin:
        if i in t1:
            s1.append(1)
        else:
            s1.append(0)
        if i in t2:
            s2.append(1)
        else:
            s2.append(0)

    minhash = mlsh.MinHasher(s1, s2)
    # print(*minhash)
    return mlsh.LSH(*minhash, 20)


def affection(tweet):
    ntrvl = 86400000
    k = 3 # shingle Size
    d1 = mlsh.shingler(preprocess(tweet.text), k)
    followers = tweet.user.followers()
    affected_followers = set()
    for i in followers:
        Ti = i.tweets(start=tweet.timestamp, interval=ntrvl)
        for t in Ti:
            d2 = mlsh.shingler(preprocess(t.text), k)
            if similarity(d1, d2):
                print("\nid:", tweet.Id)
                affected_followers.add(i)
                break
    FfCount = set()
    for i in affected_followers:
        FfCount.union(set(i.followers()))
    FfCount.union(affected_followers)
    FfCount = len(FfCount)
    if FfCount != 0:
        print(tweet.user.screen_name, tweet.Id)
    try:
        Ti = mt.TInfluence.objects.filter(tweet=tweet).get()
        Ti.sf_similarities = FfCount
        Ti.save()
    except:
        mt.TInfluence(
            tweet=tweet,
            sf_similarities=FfCount
        ).save()


timer.start()
timer._total = mt.tweet.objects.filter(Q(is_reply=False) & Q(is_quote=False) & Q(is_retweet=False)).count()

##########
passed = 0
##########

_ = passed
page_nb = 1
items_per_page = 100
offset = (page_nb - 1) * items_per_page
lst = mt.tweet.objects.filter(Q(is_reply=False) & Q(is_quote=False) & Q(is_retweet=False)).skip( offset+passed ).limit( items_per_page ).timeout(False) #.noCursorTimeout()

while lst:
    offset = (page_nb - 1) * items_per_page
    lst = mt.tweet.objects.filter(Q(is_reply=False) & Q(is_quote=False) & Q(is_retweet=False)).skip( offset+passed ).limit( items_per_page ).timeout(False)#.noCursorTimeout()
    page_nb += 1
    for t in lst:
        # input('paused, press any key to continue')
        _ += 1
        if _ < passed:
            continue
        else:
            # try:
            if mt.TInfluence.objects.filter(tweet=t).count() == 0:
                # print("triplet...")
                triplet(t)
            else:
                # print("affection...")
                if t.user.LenFollowers() != 0:
                    affection(t)
            # except :
                # print('\nERROR\n')
        timer.tick()
        timer.loading()

print("\nDone.\n")
timer.end()
timer.printlog()
