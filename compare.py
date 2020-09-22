from functools import partial
from pytomo3d.signal import process_stream
from pypers.utils import process
from obspy import read_inventory, Stream
from scipy.fftpack import fft, fftfreq


nt = 36160
dt = 0.2


obs_flags = {
    'remove_response_flag': True,
    'water_level': 100.0,
    'filter_flag': True,
    'pre_filt': [0.0188, 0.0250, 0.0588, 0.0735],
    'resample_flag': True,
    'sampling_rate': 5,
    'taper_type': "hann",
    'taper_percentage': 0.05,
    'rotate_flag': True,
    'sanity_check': True
}

syn_flags = {
    'remove_response_flag': False,
    'filter_flag': True,
    'pre_filt': [0.0188, 0.0250, 0.0588, 0.0735],
    'resample_flag': True,
    'sampling_rate': 5,
    'taper_type': "hann",
    'taper_percentage': 0.05,
    'rotate_flag': True,
    'sanity_check': False
}


def read_station(event, stream):
    station = stream[0].stats.network + '.' + stream[0].stats.station
    return read_inventory('eu_data_repo/station/' + event + '/' + station + '.xml')


def process_pair(event, syn, obs):
    inv = inventory=read_station(event, obs)
    syn = process_stream(syn, inventory=inv, **syn_flags)

    assert syn[0].stats.npts == nt
    assert syn[0].stats.delta == dt

    # try:
    #     obs = Stream([
    #         obs.select(component='N')[0],
    #         obs.select(component='E')[0],
    #         obs.select(component='Z')[0]])

    #     obs.trim(starttime=syn[0].stats.starttime)
    #     obs.resample(syn[0].stats.sampling_rate)

    #     for tr in obs:
    #         if tr.stats.npts > nt:
    #             tr.data = tr.data[:nt]
            
    #         elif tr.stats.npts < nt:
    #             print('???')


    #     obs = process_stream(obs, inv, **obs_flags)

    #     # for cmp in ('R', 'T', 'Z'):
    #     #     synt = syn.select(component=cmp)[0]
    #     #     obst = obs.select(component=cmp)[0]


    # except:
    #     pass

def process_event(event):
    src_syn = 'raw_syn/' + event + '.raw_syn.h5'
    src_obs = 'raw_obs/' + event + '.raw_obs.h5'
    dst_syn = 'proc_syn/' + event + '.proc_syn.h5'
    dst_obs = 'proc_obs/' + event + '.proc_obs.h5'

    with open('CMT/CMT.190/' + event, 'r') as f:
        lines = f.readlines()

        flags = {
            'event_latitude': float(lines[4].split()[-1]),
            'event_longitude': float(lines[5].split()[-1])}

        obs_flags.update(flags)
        syn_flags.update(flags)
        
    
    # process((src_syn, src_obs), dst_syn, partial(process_synthetic, event), 'stream', output_tag='proc_syn')
    process((src_syn, src_obs), dst_obs, partial(process_pair, event), 'stream', output_tag='proc_obs')

from mpi4py import MPI
from time import time
rank = MPI.COMM_WORLD.Get_rank()

start = time()
process_event('C201105192015A')
if rank == 0:
    print(f'{time()-start:.2f}s')
