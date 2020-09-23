from mpi4py import MPI
from time import time
from pypers.utils import process
from pyasdf import ASDFDataSet

rank = MPI.COMM_WORLD.Get_rank()

def proc(trace):
    trace.filter('lowpass', freq=1/40)
    return trace


start = time()
process('syn.h5', 'out.h5', process)
if rank == 0:
    print(f'{time()-start:.2f}s')
