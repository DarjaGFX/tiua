from mongoengine import *
import minitter as mt
from Settings import *

connect(DBNAME)
total = 1468211496

# GRAPH_PATH
# EXISTING_IDS_PATH

# def checkUsers(u1, u2):
#     """
#     gets followee and follower, checks if they exist in database, then create/update them
#     """
#     try:
#         user1 = mt.User.objects.filter(Q(Id = u1) & Q(screen_name_ne = '')).get()
#     except:
#         user1 = mt.User(Id = u1)
#     try:
#         user2 = mt.User.objects.filter(Id = u2).get()
#     except:
#         try:
#             user2 = mt.User(Id = u2)
#             user2.save()
#         except:
#             print(u2)
#     user1.followers.append(user2.id)
#     user1.save()
#
# r = open(GRAPH_PATH, 'r')
# line = r.readline()
# while line:
#     try:
#         i2d = line.split("\t")
#         id1 = i2d[0].replace('\n','')
#         id2 = i2d[1].replace('\n','')
#         checkUsers(int(id1), int(id2))
#         line = r.readline()
#     except:
#         r.close()
#         break

def checkUsers(u1, u2):
    """
    gets followee and follower, checks if they exist in database, then create/update them
    """
    if type(u1) == int:
        try:
            user1 = mt.User.objects.filter(Id = u1).get()
        except:

            return None
    else:
        user1 = u1
    try:
        user2 = mt.User.objects.filter(Id = u2).get()
    except:
        return user1
    mt.follows(
        followee= user1,
        follower= user2
    ).save()
    return user1

r = open(GRAPH_PATH, 'r')
line = r.readline()
_ = 1
##### avoid IO #####
lastId = None
user1 = None
##### & SpeedUp #####
while line:
    try:
        i2d = line.split("\t")
        id1 = i2d[0].replace('\n','')
        id2 = i2d[1].replace('\n','')
        if lastId == id1:
            if not user1:
                pass
            else:
                checkUsers(user1, int(id2))
        else:
            user1 = checkUsers(int(id1), int(id2))
            lastId = id1
    except:
        pass
    try:
        line = r.readline()
    except:
        break

    print('\r line {} of {} | {}%{}'.format(_,total , _*100/total,' '*10),end='\r')
    _ += 1
r.close()
