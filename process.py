from pytomo3d.signal import process_stream
from pypers.utils import process


event = 'C201105192015A'
syn = 'raw_syn/' + event + '.raw_syn.h5'
obs = 'raw_obs/' + event + '.raw_obs.h5'
dst = 'proc.h5'


def proc(syn, obs):
    print(len(syn), len(obs))


process((syn, obs), dst, proc, 'stream')
