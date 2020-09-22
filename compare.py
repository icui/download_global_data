from functools import partial
from pytomo3d.signal import process_stream
from pypers.utils import process
from obspy import read_inventory, Stream


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


def process_observed(event, syn, obs):
    obs = Stream([
        obs.select(component='N')[0],
        obs.select(component='E')[0],
        obs.select(component='Z')[0]])
    
    print(len(obs))
    # return process_stream(obs, inventory=read_station(event, obs), **obs_flags)


def process_synthetic(event, syn, obs):
    return process_stream(syn, inventory=read_station(event, syn), **syn_flags)


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
    process((src_syn, src_obs), dst_obs, partial(process_observed, event), 'stream', output_tag='proc_obs')


process_event('C201105192015A')
