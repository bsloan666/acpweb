import json

def parse(fname):
    handle=open(fname,'r')
    spectrum = json.load(handle)
    handle.close()
    for sample in spectrum['data_points'][0]['spectrumPoints']:
        nm = int(str(sample.keys()[0]))
        print nm,sample[sample.keys()[0]]

