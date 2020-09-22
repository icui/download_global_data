from pyasdf import ASDFDataSet


with ASDFDataSet('traces.h5', mode='r', mpi=False) as ds:
    # iterate through stations
    for station in ds.waveforms.list():
        # waveform accessor
        wav = ds.waveforms[station]

        # waveform tag
        tag = wav.get_waveform_tags()[0]

        # obspy stream
        stream = wav[tag]

        print(stream)
