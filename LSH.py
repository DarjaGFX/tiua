import numpy as np
from random import randint

HASHCOUNT = 200
THREASHOLD = 0.40


def shingler(Document=None, k=1, Type='char'):
    """
    turn `Document` into its SHINGLES
    `Type` can be `char` or `word`
    """
    res = set()
    if Document is None or k < 1:
        return None
    elif Type == 'char':
        for i in range(len(Document)-k+1):
            res.add(Document[i:i+k])
    elif Type == 'word':
        docset = Document.split()
        for i in range(len(docset)-k+1):
            res.add(' '.join(docset[i:i+k]))
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
        set_length = len(sets[0])
    except:
        return None
    for i in sets:
        try:
            if type(i) != t or len(i) != set_length:
                return None
        except:
            return None
    Signatures = np.ones([len(sets), HASHCOUNT])*set_length
    for i in range(set_length):
        PermutedOrder = np.ndarray.tolist(np.random.permutation(set_length))
        for j, s in enumerate(sets):
            if s[i] == 1:
                for x in range(HASHCOUNT):
                    print("{:,} of {:,}".format((i*len(sets)*HASHCOUNT)+(j*HASHCOUNT)+x, len(sets)*HASHCOUNT*set_length), end='\r')
                    if Signatures[j][x] > PermutedOrder[x]:
                        Signatures[j][x] = PermutedOrder[x]
    print('\n')
    return Signatures


def finalize_buckets(lv):
    final_buckets = set()
    while len(lv) > 0:
        tmp = set()
        lst = list(lv)
        for i in lst[0]:
            tmp.add(i)
        lv.remove(lst[0])
        doubleCheckFlag = 0
        while len(lv) > 0:
            if doubleCheckFlag >= 2:
                break
            changeFlag = False
            remove_candidate = None
            break_flag = False
            for item in lv:
                for element in item:
                    if element in tmp:
                        for i in item:
                            tmp.add(i)
                        remove_candidate = item
                        changeFlag = not changeFlag
                        break_flag = True
                        break
                if break_flag:
                    break
            if break_flag:
                lv.remove(remove_candidate)
            if not changeFlag:
                doubleCheckFlag += 1
        final_buckets.add(frozenset(tmp))
    return final_buckets


def LSH(*sets, bands=1):
    if len(sets[0]) % bands != 0:
        raise ValueError(f"bands can't be {bands} while hashCount is {len(sets[0])}")

    buckets = set()
    r = int(len(sets[0])/bands)
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
    return finalize_buckets(buckets)


def LSH_Value(*sets, k=1, Type='char', bands=1, HashCount=HASHCOUNT, bucket_Similarity_Threashold=0.8):
    import datetime  # ##################################### test
    print(datetime.datetime.now())  # ##################################### test
    global HASHCOUNT
    HASHCOUNT = HashCount
    global THREASHOLD
    THREASHOLD = bucket_Similarity_Threashold
    # get shingls for all Docs
    print("START SHINGLING...")
    shingl = [shingler(i, k, Type) for i in sets]
    print("SHINGLING FINISHED.")
    # feeding MinHasher
    print("START FEEDING MINHASHER...")
    unin = set()
    for i in shingl:
        unin.update(i)
    print(f"vector size: {len(unin)}")  # ############################## test
    s = [[] for i in shingl]
    for i in unin:
        for indx, sh in enumerate(shingl):
            if i in sh:
                s[indx].append(1)
            else:
                s[indx].append(0)
    print('START MINHASHING...')
    minhash = MinHasher(*s)
    import numpy as np
    np.save('mnhsh', minhash)
    print('MINHASHING FINISHED.')
    print('START BUCKETING...')
    # pass to LSH and return
    print(datetime.datetime.now())  # ##################################### test
    return LSH(*minhash, bands=bands)
