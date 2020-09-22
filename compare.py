from functools import partial
from pytomo3d.signal import process_stream
from pypers import Space
from pypers.utils import process, AuxiliaryData
from obspy import read_inventory, Stream
from scipy.fftpack import fft, fftfreq
from pyasdf import ASDFDataSet
import numpy as np
import cmath

from mpi4py import MPI
from time import time
rank = MPI.COMM_WORLD.Get_rank()

nt = 36160
dt = 0.2
freq = fftfreq(nt, dt)
fwin = np.squeeze(np.where((freq > 1/100) & (freq < 1/40)))
phase = np.vectorize(cmath.phase)


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


def process_pair(event, syn, obs):
    sta = syn[0].stats.network + '.' + syn[0].stats.station
    inv = read_inventory('eu_data_repo/station/' + event + '/' + sta + '.xml')
    syn = process_stream(syn, inventory=inv, **syn_flags)
    chosen = []

    try:
        obs = Stream([
            obs.select(component='N')[0],
            obs.select(component='E')[0],
            obs.select(component='Z')[0]])

        obs.trim(starttime=syn[0].stats.starttime)
        obs.resample(syn[0].stats.sampling_rate)

        for tr in obs:
            if tr.stats.npts > nt:
                tr.data = tr.data[:nt]

        obs = process_stream(obs, inv, **obs_flags)

        for cmp in ('R', 'T', 'Z'):
            synt = syn.select(component=cmp)[0]
            obst = obs.select(component=cmp)[0]

            ft_syn = fft(synt.data)[fwin]
            ft_obs = fft(obst.data)[fwin]

            if np.std(phase(ft_obs / ft_syn)) < 0.4:
                chosen.append(cmp)

    except:
        pass

    if len(chosen):
        return AuxiliaryData(parameters={'components': chosen})


def process_event(event):
    src_syn = 'raw_syn/' + event + '.raw_syn.h5'
    src_obs = 'raw_obs/' + event + '.raw_obs.h5'
    dst = 'std/' + event + '.std.h5'

    with open('CMT/CMT.190/' + event, 'r') as f:
        lines = f.readlines()

        flags = {
            'event_latitude': float(lines[4].split()[-1]),
            'event_longitude': float(lines[5].split()[-1])}

        obs_flags.update(flags)
        syn_flags.update(flags)
        
    process((src_syn, src_obs), dst, partial(process_pair, event), 'stream', output_tag='selected')
    MPI.COMM_WORLD.Barrier()
    
    if rank == 0:
        with ASDFDataSet(dst, mode='r', mpi=False) as ds:
            nselected = len(ds.auxiliary_data.selected.list())

            if nselected > 10:
                with open('selected.txt', 'a') as f:
                    f.write(f'{event} {nselected}\n')


for event in Space('CMT/CMT.190').ls():
    try:
        process_event(event)
    
    except Exception as e:
        print(e)
