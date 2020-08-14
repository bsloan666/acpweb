import coordvector
import spectrum
import observer

class SpectralLocus(object):
    def __init__(self, cmf):
        self.data = {}
        dummy = spectrum.Spectrum()
        for i in range(dummy.start, dummy.end+1): 
            sm = spectrum.Spectrum()
            for j in range(sm.start, sm.end+1): 
                if j == i:
                    sm.data[j-sm.start] = 4000.00 
                else:
                    sm.data[j-sm.start] = 0.0

            (x,y,z) = cmf.convert(sm, dummy)
            (X,Y,Z) = cmf.normalize(x,y,z)
            self.data[i] = coordvector.CoordVector(X, Y, Z)
        self.valid = True    

    def sample(self,nm): 
        if not self.valid:
            return coordvector.CoordVector(0.3, 0.3, 0.3)
        if nm in self.data.keys():
            return self.data[nm]
        else:
            return coordvector.CoordVector(0.3, 0.3, 0.3)

