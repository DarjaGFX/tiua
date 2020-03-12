import numpy as np
from PermutationHashFunctions import *

HASHFUNCTIONS = [H1 , H2]

def shingler(Document= None , k = 1):
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
    Signature = [l for x in range(len(HASHFUNCTIONS))]
    Signatures = [Signature for x in range(len(sets))]
    Signatures = np.array(Signatures)
    for i in lineNumber:
        PermutedOrder = []
        for h in HASHFUNCTIONS:
            PermutedOrder.append(h(i))
        for j,s in enumerate(sets):
            if s[i] == 1:
                for x in range(len(HASHFUNCTIONS)):
                    if Signatures[j,x] > PermutedOrder[x]:
                        Signatures[j,x] = PermutedOrder[x]

    return Signatures


a = [1,0,1,1,0]
b = [0,1,1,0,1]

for i,j in enumerate(MinHasher(a,b)):
    print('set{}'.format(i), j)
