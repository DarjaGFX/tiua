import numpy as np
from random import randint

HASHCOUNT = 200
THREASHOLD = 0.6


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
                    if Signatures[j][x] > PermutedOrder[x]:
                        Signatures[j][x] = PermutedOrder[x]

    return Signatures


def LSH(*sets, bands=1):
    if len(sets[0]) % bands != 0:
        raise ValueError("bands can't be {}".format(bands))

    buckets = set()
    r = len(sets[0])/bands
    for b in range(bands):
        low = int(b*r)
        up = int((b+1)*r)
        if type(low) != int or type(up) != int:
            print(type(low))
            print(type(up))
        for fs in range(len(sets)-1):
            for ss in range(fs+1, len(sets)):
                if {ss, fs} in buckets:
                    continue
                shared = 0
                for i in range(low, up):
                    if sets[fs][i] == sets[ss][i]:
                        shared += 1
                if float(shared)/r >= THREASHOLD:
                    buckets.add(frozenset({fs, ss}))
    return buckets
