"""

sort using np.argsort. Much faster than: sorted(zip(ages, height))


"""

import numpy as np
from __future__ import print_function

ages = np.random.randint(low=30, high=80, size=10)
height = np.random.randint(low=150, high=210, size=10)

# sort by age
sorter = np.argsort(ages)
print(ages[sorter])
print(height[sorter])


# np.argsort versus np.sort
data = np.random.randint(low=0, high=1000, size=1000)

import time
for kind in ['quicksort', 'mergesort', 'heapsort']:
    print(kind)
    timeNow = time.time()
    [np.sort(data, kind=kind)for _ in range(10000)]
    print("time pased: {:.6f}".format(time.time() - timeNow))

    timeNow = time.time()
    [np.argsort(data, kind=kind)for _ in range(10000)]
    print("time pased: {:.6f}".format(time.time() - timeNow))


