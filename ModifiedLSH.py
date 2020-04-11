import numpy as np
from random import randint

HASHCOUNT = 20


def shingler(Document=None, k=1):
    if Document is None or k < 1:
        return None
    else:
        res = set()
        for i in range(len(Document)-k+1):
            res.add(Document[i:i+k])
        return res


def MinHasher(*sets):
    """
    returns signature of all given binary `sets`.
    `sets` should be binary lists, and equal in length.

    Ex.
    set1 = [1,0,0,1,0,1,1,0,0]
    set2 = [0,1,1,1,0,1,1,1,1]
    set3 = [1,0,1,0,1,0,1,0,1]
    for i,j in enumerate(MinHasher(set1, set2, set3)):
        print('set{}'.format(i), j)
    """
    try:
        t = type(sets[0])
        l = len(sets[0])
    except:
        return None
    for i in sets:
        try:
            if type(i) != t or len(i) != l:
                return None
        except:
            return None

    lineNumber = list(range(l))
    HashOrders = [set(lineNumber) for x in range(HASHCOUNT)]
    Signature = [l for x in range(HASHCOUNT)]
    Signatures = [Signature for x in range(len(sets))]
    Signatures = np.array(Signatures)
    for i in lineNumber:
        PermutedOrder = []
        for h in range(HASHCOUNT):
            ind = randint(0, len(HashOrders[h])-1)
            order = list(HashOrders[h])[ind]
            HashOrders[h].remove(order)
            PermutedOrder.append(order)
        for j, s in enumerate(sets):
            if s[i] == 1:
                for x in range(HASHCOUNT):
                    if Signatures[j, x] > PermutedOrder[x]:
                        Signatures[j, x] = PermutedOrder[x]

    return Signatures


a = [1, 0, 1, 1, 0]
b = [0, 1, 1, 0, 1]

minsh = MinHasher(a, b)
for i, j in enumerate(minsh):
    print('set{}'.format(i), j)

shared = 0
for i in range(HASHCOUNT):
    if minsh[0][i] == minsh[1][i]:
        shared += 1
print(shared, float(shared)/HASHCOUNT)
