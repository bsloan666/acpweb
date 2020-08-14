#!/usr/bin/env python
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import tempfile
import math 
import spectrum
import locus
import observer

jumps = [30,50,50,50,50,50,50,50,50,50,50,50,50,50]

def plot_spectrum(img, draw,  sm, color, margin, scale):

    width = img.size[0]
    height = img.size[1]

    
    iprop = float (width) / 360
    offset = 370
    lastx = 0.0 
    lasty = 0.0

    if scale < 0.00001: 
        max  = sm.max()
        scale = (height * margin) / max    
       
    
    for nm in range( 370, 731):
        val = sm.sample(nm)*scale + 16
        draw_line( draw, img, (nm - offset) * iprop, 
                     height - val, 
                     lastx, 
                     height - lasty, color)
        lastx = (nm - offset) * iprop
        lasty = val

    return scale;

def draw_plot_field(image, draw, sl):
    c = (60,60,60)
    draw.rectangle((0,0,image.size[0], image.size[1]),fill=c)
    fnt = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 12)

    width = image.size[0]
    height = image.size[1]
    tic = 0
    hincr = height/10.0

    iprop = float(width)/360.0
    offset = 370
    lastx = 0.0 

    for nm in range(370, 731, 4):
        coordrgb = sl.sample(nm)
        color = (coordrgb.r8,coordrgb.g8,coordrgb.b8)
        xpos = int((nm-offset) * iprop)
        draw.rectangle((lastx,
            height-16, xpos, height), fill=color)
        lastx = xpos
    
    nm = 370
    while nm < 730:
        xpos = int((nm-offset) * iprop)
        color =  (85,85,85)
        draw.line((xpos, 0.0, xpos, float(height-16)), fill=color)
        brite =  int(abs(550 - nm)/180.0 * 255.0) 
        color = (brite, brite, brite)
        draw.text((xpos - 12, height-14), str(nm),font=fnt, fill=color)
        nm = nm + jumps[tic]
        tic = tic+1

    ii = 0.099999
    voff = hincr

    while   ii < 1.0:
        color = (85,85,85)
        draw.line((0.0, voff, width - 42.0, voff), fill=color);
        color = (128,128,128)
        draw.text((width-36, voff - 8), str(1.0 - ii)[0:3],font=fnt, fill=color );
        ii += 0.1
        voff += hincr
  

def draw_plot( ref , test):
    img = Image.new('RGB',(640,260),color=(80,80,80))
    draw = ImageDraw.Draw(img)

    cmf = observer.ColorMatchingFunction()
    sl = locus.SpectralLocus(cmf)

    draw_plot_field(img, draw,sl)

    handle = open('cie_x.json','r')
    X = spectrum.Spectrum()
    X.from_file(handle)
    handle.close()

    handle = open('cie_y.json','r')
    Y = spectrum.Spectrum()
    Y.from_file(handle)
    handle.close()

    handle = open('cie_z.json','r')
    Z = spectrum.Spectrum()
    Z.from_file(handle)
    handle.close()
    
    scale  = plot_spectrum(img, draw, Z, (0,0,255, 255), 0.85,  0.0)           
    plot_spectrum(img, draw, Y, (0,255,0, 255), 0.85,  scale)           
    plot_spectrum(img, draw, X, (255,0,0, 255), 0.85,  scale)          
    plot_spectrum(img, draw, ref, (255,255,0, 255), 0.85, 0.0)
    plot_spectrum(img, draw, test, (255,255,255, 255), 0.85, 0.0)

    tmp = tempfile.TemporaryFile()
    img.save(tmp, format='png')
    tmp.seek(0)
    sludge = tmp.read()
    return sludge

def plot(draw, img, x, y, c, col,steep):
    if steep:
        x,y = y,x
    if x < img.size[0] and y < img.size[1] and x >= 0 and y >= 0:
        c = c * (float(col[3])/255.0)
        p = img.getpixel((x,y))
        draw.point((int(x),int(y)),fill=(int((p[0]*(1-c)) + col[0]*c), int((p[1]*(1-c)) + col[1]*c), int((p[2]*(1-c)) + col[2]*c),255))

def iround(x):
    return ipart(x + 0.5)

def ipart(x):
    return math.floor(x)

def fpart(x):
    return x-math.floor(x)

def rfpart(x):
    return 1 - fpart(x)


def draw_line(draw, img, x1, y1, x2, y2, col):
    dx = x2 - x1
    dy = y2 - y1

    steep = abs(dx) < abs(dy)
    if steep:
        x1,y1=y1,x1
        x2,y2=y2,x2
        dx,dy=dy,dx
    if x2 < x1:
        x1,x2=x2,x1
        y1,y2=y2,y1
    gradient = float(dy) / float(dx)

    #handle first endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend    #this will be used in the main loop
    ypxl1 = ipart(yend)
    plot(draw, img, xpxl1, ypxl1, rfpart(yend) * xgap,col, steep)
    plot(draw, img, xpxl1, ypxl1 + 1, fpart(yend) * xgap,col, steep)
    intery = yend + gradient # first y-intersection for the main loop

    #handle second endpoint
    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend    # this will be used in the main loop
    ypxl2 = ipart (yend)
    plot (draw, img, xpxl2, ypxl2, rfpart (yend) * xgap,col, steep)
    plot (draw, img, xpxl2, ypxl2 + 1, 1.0,col, steep)
    plot (draw, img, xpxl2, ypxl2 + 2, 1.0,col, steep)
    plot (draw, img, xpxl2, ypxl2 + 3, fpart (yend) * xgap,col, steep)

    #main loop
    for x in range(int(xpxl1 + 1), int(xpxl2 )):
        plot (draw, img, x, ipart (intery), rfpart (intery),col, steep)
        plot (draw, img, x, ipart (intery) + 1, 1.0,col, steep)
        plot (draw, img, x, ipart (intery) + 2, 1.0,col, steep)
        plot (draw, img, x, ipart (intery) + 3, fpart (intery),col, steep)
        intery = intery + gradient

    

