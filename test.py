from asdfy import ASDFProcessor


def process(acc):
    print(len(acc.stream), acc.station)


ASDFProcessor('traces.h5', 'proc.h5', process, input_type='stream', accessor=True)
