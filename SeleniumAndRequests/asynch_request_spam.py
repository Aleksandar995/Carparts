import grequests

try:
    from itertools import izip_longest
except ImportError:  # Python 3
    from itertools import zip_longest as izip_longest

import time


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


i = 0
f1 = open("async.txt", "a")
apis = {'apikey': 'atpvGyxKcznNy'}
with open("requests.txt") as f:
    for lines in grouper(f, 10, ''):
        assert len(lines) == 10
        start = time.time()
        rs = (grequests.get(u, headers=apis) for u in lines)

        end = time.time()
        i = i + 10
        print("Ran" + str(i) + "requests" + "time" + str(end-start))
        f1.write(str(grequests.map(rs)) + '\n')

