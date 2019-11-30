import numpy as np
from Settings import *

total = 1468211496
_ = 1
r = open(GRAPH_PATH, 'r')
ids = set()
print('Get Unique ids\n')
line = r.readline()
while line:
    try:
        _ += 1
        i2d = line.split('\t')
        ids.add(int(i2d[0].replace('\n','')))
        ids.add(int(i2d[1].replace('\n','')))
        print('\r line {} of {} | {}%{}'.format(_,total , _*100/total,' '*10),end='\r')
        line = r.readline()
    except:
        try:
            line = r.readline()
        except:
            break
        continue
print('\nDone.\n')
np.save('base_ids', ids)
