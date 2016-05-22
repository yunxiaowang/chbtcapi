import json


def Nup(HH, HC, LC, LL, end, k1):
    R = max(HH - LC, HC - LL)
    return end + R * k1


def Ndown(HH, HC, LC, LL, end, k2):
    R = max(HH - LC, HC - LL)
    return end - R * k2


def calc(r, N, k1, k2):
    # print len(r)
    if len(r) <= 5:
        return

    cny = 100.0
    eth = 0.0
    op = []

    length = len(r)
    # print length
    for i in xrange(3, length):
        # print i
        HH = 0.0
        HC = 0.0
        LC = 99999999.9
        LL = 99999999.9
        for j in xrange(i - N, i):
            if r[j][2] > HH:
                HH = r[j][2]
            if r[j][4] > HC:
                HC = r[j][4]
            if r[j][4] < LC:
                LC = r[j][4]
            if r[j][3] < LL:
                LL = r[j][3]

        up = Nup(HH, HC, LC, LL, r[i - 1][4], k1)
        down = Ndown(HH, HC, LC, LL, r[i - 1][4], k2)

        y1 = r[i]
        start1 = y1[1]
        high1 = y1[2]
        low1 = y1[3]
        end1 = y1[4]
        if end1 > start1:
            if low1 < down:
                if eth > 0.01:
                    cny += eth * down
                    eth = 0.0
                    op.append(['sell', down])
            if high1 > up:
                if cny > 0.01:
                    eth += cny / up
                    cny = 0.0
                    op.append(['buy', up])
        else:
            if high1 > up:
                if cny > 0.01:
                    eth += cny / up
                    cny = 0.0
                    op.append(['buy', up])
            if low1 < down:
                if eth > 0.01:
                    cny += eth * down
                    eth = 0.0
                    op.append(['sell', down])

    if eth > 0.01:
        cny += eth * end1

    return cny, op

# N = 4
kk1 = (65, 85)
kk2 = (65, 85)

if __name__ == '__main__':
    f = open('5min.txt')
    s = f.read()
    d = json.loads(s)
    t = {}
    nn = 0

    for N in xrange(1, 3):
        mres = 0.0
        mk1 = 0.0
        mk2 = 0.0
        mop = None
        cc = 0

        for k1 in xrange(kk1[0], kk1[1] + 1):
            for k2 in xrange(kk2[0], kk2[1] + 1):
                res, op = calc(d, N, k1 / 100.0, k2 / 100.0)
                # print k1, k2, res
                if (k1, k2) not in t:
                    t[(k1, k2)] = [res, ]
                else:
                    t[(k1, k2)].append(res)

                if res > 100.0:
                    cc += 1

                if res > mres:
                    mres = res
                    mk1 = k1
                    mk2 = k2
                    mop = op
        print 'N: ', N
        print 'mres: ', mres
        print 'mk1:', mk1
        print 'mk2:', mk2
        print 'cc:', cc
        print '------------------'
    rr = []
    for k, v in t.iteritems():
        if v > 100.0:
            rr.append([k[0], k[1], v])
            # print k, v

    def myCmp(a, b):
        if len(a) == 1:
            return -1 if a[2][0] < b[2][0] else 1
        else:
            t1 = 0
            t2 = 0
            for i in xrange(0, len(a)):
                t1 += a[2][0]
                t2 += b[2][0]
            return -1 if t1 < t2 else 1
    rr = sorted(rr, cmp=myCmp, reverse=True)
    # rr = rr[: 20]
    print rr
    # print 'mop', mop
    # res = calc(d, 1, 0.7, 0.7)
    # print res
    # print s
