from pytomo3d.signal import process_stream
from pypers.io import process
from proc import proc


event = 'C201105192015A'
syn = 'raw_syn/' + event + '.raw_syn.h5'
obs = 'raw_obs/' + event + '.raw_obs.h5'
dst = 'proc.h5'


process((syn, obs), dst, proc, 'stream').run()
