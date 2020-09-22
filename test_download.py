import os
import obspy
from download_util import download_event, convert_event


def download_convert(eventname):
    eventfile = os.path.join("CMT/CMT.190", eventname)
    event = obspy.read_events(eventfile)[0]

    basedir = "./eu_data_repo"
    waveform_base = os.path.join(basedir, "waveform")
    station_base = os.path.join(basedir, "station")
    asdf_base = os.path.join(basedir, "asdf")
    stationfile = os.path.join("CMT/STATIONS.190", 'STATION.' + eventname)
    stations = set()
    networks = set()
    stas = set()
    
    with open(stationfile, 'r') as f:
        for line in f.readlines():
            sta, net = line.split()[:2]
            networks.add(net)
            stas.add(sta)
            stations.add(net + '.' + sta)

    params = {
        "starttime_offset": -600,
        "endtime_offset": 11000,
        "networks": list(networks),
        "stations": list(stas),
        "channels": None,
        "location_priorities": ["", "00", "10"],
        "channel_priorities": ["BH[ZNE]", "HH[ZNE]"],
        "providers": None
    }

    download_event(eventname, event, params, waveform_base, station_base)
    convert_event(eventname, stations, waveform_base, asdf_base)


if __name__ == "__main__":
    from pypers import Space

    ws = Space()

    for event in ws.ls('CMT/CMT.190'):
        if not ws.has('eu_data_repo/asdf/' + event + '.raw_obs.h5'):
            try:
                download_convert(event)
            
            except:
                with open('failed.txt', 'a') as f:
                    f.write(event + '\n')
    