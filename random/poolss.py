import sys
import numpy as np
import time
import multiprocessing

class SerialPool(object):

    def close(self):
        return

    def map(self, *args, **kwargs):
        return map(*args, **kwargs)


def get_pool(mpi=False, threads=1):

    if mpi:
        from emcee.mpi_pool import MPIPool

        pool = MPIPool()

        if not pool.is_master():
            pool.wait()
            sys.exit(0)
    elif threads > 1:
        pool = multiprocessing.Pool(threads)
    else:
        pool = SerialPool()
    return pool
