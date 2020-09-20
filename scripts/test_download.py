import os
import obspy
from download_util import download_event


if __name__ == "__main__":
    eventname = "C201105192015A"
    eventfile = os.path.join("../CMT/CMT.190", eventname)
    event = obspy.read_events(eventfile)[0]

    params = {
        "starttime_offset": -600,
        "endtime_offset": 11000,
        "networks": ["FR"],
        "channels": None,
        "location_priorities": ["", "00", "10"],
        "channel_priorities": ["BH[ZNE12]", "HH[ZNE12]"],
        "providers": None
    }

    basedir = "./test_data_repo"
    waveform_base = os.path.join(basedir, "waveform")
    station_base = os.path.join(basedir, "station")

    download_event(eventname, event, params, waveform_base, station_base)
