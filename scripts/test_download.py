import os
import obspy
from download_util import download_event, convert_event


def download_convert(eventname):
    eventfile = os.path.join("CMT/CMT.190", eventname)
    event = obspy.read_events(eventfile)[0]

    params = {
        "starttime_offset": -600,
        "endtime_offset": 11000,
        "networks": ["FR"],
        "channels": None,
        "location_priorities": ["", "00", "10"],
        "channel_priorities": ["BH[ZNE]", "HH[ZNE]"],
        "providers": None
    }

    basedir = "./eu_data_repo"
    waveform_base = os.path.join(basedir, "waveform")
    station_base = os.path.join(basedir, "station")
    asdf_base = os.path.join(basedir, "asdf")
    stationfile = os.path.join("CMT/STATIONS.190", 'STATION_' + eventname[1:])

    # download_event(eventname, event, params, waveform_base, station_base)
    convert_event(eventname, stationfile, waveform_base, asdf_base)

if __name__ == "__main__":
    download_convert("C201105192015A")
    