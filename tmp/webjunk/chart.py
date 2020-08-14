import spectrum

class ChipChart(object):
    def __init__(self):
        self.patches = []
        self.ncolumns = 6
        self.nrows  = 4
        
        file_pat ="resources/macbeth/gmcc_%02d.json"
        for i in range(0,24):
            handle = open(file_pat%i, 'r')
            sp = spectrum.Spectrum()
            sp.from_file(handle)
            self.patches.append(sp)
            handle.close()
