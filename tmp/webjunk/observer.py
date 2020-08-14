import math
import spectrum

class ColorMatchingFunction(object): 
    def __init__(self):  

        self.wb_X = 1.0
        self.wb_Y = 1.0
        self.wb_Z = 1.0

        handle = open('cie_x.json','r')
        self.my_ciex_func = spectrum.Spectrum()
        self.my_ciex_func.from_file(handle)
        handle.close()

        handle = open('cie_y.json','r')
        self.my_ciey_func = spectrum.Spectrum()
        self.my_ciey_func.from_file(handle)
        handle.close()

        handle = open('cie_z.json','r')
        self.my_ciez_func = spectrum.Spectrum()
        self.my_ciez_func.from_file(handle)
        handle.close()

    def white_balance(self, illum):
        self.wb_X = 1.0
        self.wb_Y = 1.0
        self.wb_Z = 1.0

    
        white = spectrum.Spectrum()
        refl = spectrum.Spectrum()
        rr = spectrum.Spectrum()
        gg = spectrum.Spectrum()
        bb = spectrum.Spectrum()

        spectrum.mult2(white, illum, refl);  

        spectrum.mult2( self.my_ciex_func, refl, rr);
        spectrum.mult2( self.my_ciey_func, refl, gg);
        spectrum.mult2( self.my_ciez_func, refl, bb);
   
        self.wb_X = rr.power(); 
        self.wb_Y = gg.power(); 
        self.wb_Z = bb.power();


    def convert(self, smap, illum): 
               
        xx = spectrum.Spectrum()
        yy = spectrum.Spectrum()
        zz = spectrum.Spectrum()
        refl = spectrum.Spectrum()

        spectrum.mult2(smap, illum, refl)  

        spectrum.mult2( self.my_ciex_func, refl, xx)
        spectrum.mult2( self.my_ciey_func, refl, yy)
        spectrum.mult2( self.my_ciez_func, refl, zz)

        X = xx.power()/self.wb_X
        Y = yy.power()/self.wb_Y
        Z = zz.power()/self.wb_Z

        return (X, Y, Z)

    def normalize(self, X,Y,Z):
        x = 0.0
        y = 0.0
        z = 0.0
        if X < 0.000001 and Y < 0.000001 and Z < 0.000001:
            x = X
            y = Y
            z = Z
        else:
            x = X/(X+Y+Z)
            y = Y/(X+Y+Z)
            z = Z/(X+Y+Z)

        return (x,y,z) 




