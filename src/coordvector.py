import math

srgb_curve = [
0, 12, 21, 28, 33, 38, 42, 46, 49, 52, 55, 58, 61, 63, 66, 68, 
70, 73, 75, 77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 94, 96, 97, 
99, 100, 102, 103, 105, 106, 107, 109, 110, 111, 112, 114, 115, 116, 117, 119, 
120, 121, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 133, 134, 135, 136, 
137, 138, 139, 140, 141, 142, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 
151, 152, 153, 154, 155, 156, 157, 157, 158, 159, 160, 161, 161, 162, 163, 164, 
165, 165, 166, 167, 168, 168, 169, 170, 171, 171, 172, 173, 174, 174, 175, 176, 
176, 177, 178, 179, 179, 180, 181, 181, 182, 183, 183, 184, 185, 185, 186, 187, 
187, 188, 189, 189, 190, 191, 191, 192, 193, 193, 194, 194, 195, 196, 196, 197,
198, 198, 199, 199, 200, 201, 201, 202, 202, 203, 204, 204, 205, 205, 206, 206, 
207, 208, 208, 209, 209, 210, 210, 211, 212, 212, 213, 213, 214, 214, 215, 215, 
216, 217, 217, 218, 218, 219, 219, 220, 220, 221, 221, 222, 222, 223, 223, 224, 
225, 225, 226, 226, 227, 227, 228, 228, 229, 229, 230, 230, 231, 231, 232, 232, 
233, 233, 234, 234, 235, 235, 236, 236, 237, 237, 238, 238, 238, 239, 239, 240, 
240, 241, 241, 242, 242, 243, 243, 244, 244, 245, 245, 246, 246, 246, 247, 247, 
248, 248, 249, 249, 250, 250, 251, 251, 251, 252, 252, 253, 253, 254, 254, 254
] 


class CoordVector(object):
    def __init__(self, rX=0.3, rY=0.3, rZ=0.3): 
        self.X = rX
        self.Y = rY 
        self.Z = rZ 
        #yyy = self.Y

        Y_n = 100 

        Xn = 0.80
        Yn = 1.0
        Zn = 1.1

        if self.X < 0.00001 and self.Y < 0.00001 and self.Z < 0.00001:
            self.X = 0.00001
            self.Y = 0.00001
            self.Z = 0.00001

        XYZ_to_sRGB =\
            [[3.1338561, -1.6168667, -0.4906146],
            [-0.9787684,  1.9161415,  0.0334540],
            [0.0719453, -0.2289914,  1.4052427]]

        """
        #little x,y
        self.x = self.X/(self.X+self.Y+self.Z)
        self.y = self.Y/(self.X+self.Y+self.Z)

        # u', v' in terms of XYZ
        # self.ui = (4.0f * self.X) / (self.X + 15.0f * self.Y + 3.0f * self.Z);
        # self.vi = (9.0f * self.Y) / (self.X + 15.0f * self.Y + 3.0f * self.Z);
        # u', v' in terms of xy 
        self.ui = (2.0 * self.x) / (6.0 * self.y - self.x + 1.5)
        self.vi = (4.5 * self.y) / (6.0 * self.y - self.x + 1.5)
        

        # u*, v* 
        self.Wx = 25.0 * math.pow(self.Y, 0.33333) - 17.0
        self.Ux = 13.0 * self.Wx * (self.ui - (-0.0001))
        self.Vx = 13.0 * self.Wx * (self.vi - (-0.0001))

        # a*, b* 
        e = 0.008856
        k = 7.7869591
        if (self.X/Xn) > e:
            fx = math.pow(self.X/Xn, 1.0/3.0)
        else:    
            fx = k * (self.X/Xn) + 0.1379 

        if(self.Y/Yn) > e: 
            fy = math.pow(self.Y/Yn, 1.0/3.0)
        else:
            fy = k * (self.Y/Yn) + 0.1379

        if (self.Z/Zn) > e:
            fz = math.pow(self.Z/Zn, 1.0/3.0)
        else:
            fz = k * (self.Z/Zn) + 0.1379

        self.ax = 500.0 * (fx - fy) 
        self.bx = 200.0 * (fy - fz) 

        self.ax = self.ax / 500.0
        self.bx = self.bx / 500.0


        # L*
        sixtwentyninths_3 = math.pow(6.0/29.0, 3.0)
        twentyninththirds_3 = math.pow(29.0/3.0, 3.0)

        self.Lx = 0 
        if self.Y / Y_n >= sixtwentyninths_3:
            self.Lx = twentyninththirds_3 * self.Y / Y_n
        else: 
            self.Lx = 116 * math.pow(self.Y / Y_n, 0.333333) - 16.0 

        cx_over_Lx = 13 * math.sqrt(math.pow(self.ui - 0.333, 2.0) + math.pow(self.vi - 0.333, 2.0));

        self.cx = cx_over_Lx * self.Lx;

        # c*
        self.cx /= 100
        self.Lx /= 20
        """

        self.r = self.X * XYZ_to_sRGB[0][0] + self.Y * XYZ_to_sRGB[0][1] + self.Z * XYZ_to_sRGB[0][2] 
        self.g = self.X * XYZ_to_sRGB[1][0] + self.Y * XYZ_to_sRGB[1][1] + self.Z * XYZ_to_sRGB[1][2] 
        self.b = self.X * XYZ_to_sRGB[2][0] + self.Y * XYZ_to_sRGB[2][1] + self.Z * XYZ_to_sRGB[2][2]
        #print "initial Y [%f]  final Y [%f]"%(yyy, self.Y)
        self.r8 = int(srgb_curve[self.clamp_scale(self.r)])
        self.g8 = int(srgb_curve[self.clamp_scale(self.g)])
        self.b8 = int(srgb_curve[self.clamp_scale(self.b)])
        """
        self.r8 = self.clamp_scale(self.r)
        self.g8 = self.clamp_scale(self.g)
        self.b8 = self.clamp_scale(self.b)

        """
    def clamp_scale(self, in_val):
        if in_val <= 0.0:
            return 0 
        elif  in_val > 1.0:
            return  255 
        else:
            return int(in_val  * 255) 

