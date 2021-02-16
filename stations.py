from pypers import Directory
from pyasdf import ASDFDataSet
from obspy.core.inventory import Station


d = Directory('eu190')

for event in d.ls('events'):
    print(event)
    with ASDFDataSet(f'eu190/rawdata_eu190/{event}.raw_obs.h5', mode='r', mpi=False) as ds:
        lines = []
        dots = 28, 41, 55, 62

        for station in ds.waveforms.list():
            if not hasattr(ds.waveforms[station], 'StationXML'):
                print('  ' + station)
                continue

            sta: Station = ds.waveforms[station].StationXML.networks[0].stations[0]

            ll = station.split('.')
            ll.reverse()
            ll.append(f'{sta.latitude:.4f}')
            ll.append(f'{sta.longitude:.4f}')
            ll.append(f'{sta.elevation:.1f}')
            ll.append(f'{sta.channels[0].depth:.1f}')

            line = ll[0].ljust(13) + ll[1].ljust(5)

            for i in range(4):
                    num = ll[i + 2]

                    if '.' in num:
                        nint, _ = num.split('.')
                    
                    else:
                        nint = num

                    while len(line) + len(nint) < dots[i]:
                        line += ' '
                    
                    line += num
                
            lines.append(line)
        
        lines.append('')
        d.writelines(lines, f'stations/STATIONS.{event}')
