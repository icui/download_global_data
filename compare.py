from pytomo3d.signal import process_stream
from pypers.utils import process


obs_flags = {
    'remove_response_flag': True,
    'water_level': 100.0,
    'filter_flag': True,
    'pre_filt': [0.0188, 0.0250, 0.0588, 0.0735],
    'relative_starttime': 0,
    'relative_endtime': 7150,
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
    'relative_starttime': 0,
    'relative_endtime': 7150,
    'resample_flag': True,
    'sampling_rate': 5,
    'taper_type': "hann",
    'taper_percentage': 0.05,
    'rotate_flag': True,
    'sanity_check': False
}


def process_observed(syn, obs):
    pass


def process_synthetic(syn, obs):
    pass


def process_event(event):
    src_syn = 'raw_syn/' + event + '.raw_syn.h5'
    src_obs = 'raw_obs/' + event + '.raw_obs.h5'
    dst_syn = 'proc_syn/' + event + '.proc_syn.h5'
    dst_obs = 'proc_obs/' + event + '.proc_obs.h5'
    
    process((src_syn, src_obs), dst_syn, process_synthetic, 'stream', output_tag='proc_syn')
    process((src_syn, src_obs), dst_obs, process_observed, 'stream', output_tag='proc_obs')


process_event('C201105192015A')
