# time python multiprocssing_mpi.python
# time python multiprocssing_mpi.py --threads=2
# time mpiexec -n 4 python multiprocssing_mpi.py --mpi
# time mpirun -n 3 python multiprocssing_mpi.py
# time mpiexec -n 4 python multiprocssing_mpi.py --mpi

from __future__ import division, print_function

# Standard library
import sys
from poolss import get_pool
import time

def f(x):
    time.sleep(1.)
    return x**2

def main(pool):
    return pool.map(f, range(100))



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="")

    # threading
    parser.add_argument("--mpi", dest="mpi", default=False,
                        action="store_true",
                        help="Run with MPI.")
    parser.add_argument("--threads", dest="threads",
                        default=None, type=int,
                        help="Number of multiprocessing threads to run on.")

    args = parser.parse_args()
    pool = get_pool(args.mpi, args.threads)
    result = main(pool)
    pool.close()
    print(result)
    # import pdb; pdb.set_trace()


