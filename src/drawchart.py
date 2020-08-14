#!/usr/bin/env python
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import tempfile
import math 
import spectrum
import locus
import observer
import coordvector
import chart

def draw_split_chart(chart, ref, test):
    img = Image.new('RGB',(640,430),color=(0,0,0))
    draw = ImageDraw.Draw(img)

    width = img.size[0]
    height = img.size[1]
    hsize = chart.ncolumns
    vsize = chart.nrows

    cmf = observer.ColorMatchingFunction()
    cmf2 = observer.ColorMatchingFunction()

    refl = spectrum.Spectrum()
   
    cmf.white_balance(ref)
    cmf2.white_balance(test)

    block = width / hsize
    border =  int(0.125 * block)

    block = (width - (border *hsize + border))/hsize
    block2 = block/2;

    y1 = border;
    for i in range(0,vsize):
        x1 = border
        for j in range(0, hsize):
            vertindex = i 
            horindex = j
            (X,Y,Z) = cmf2.convert(chart.patches[i * hsize + j], test)
            print( X*.6, Y*.6, Z*.6)
            v = coordvector.CoordVector(X*.6,Y*.6,Z*.6)
            rr = v.r8
            gg = v.g8
            bb = v.b8

            (X,Y,Z) = cmf.convert(chart.patches[i * hsize + j], ref)
            v = coordvector.CoordVector(X*.6,Y*.6,Z*.6)
            r = v.r8
            g = v.g8
            b = v.b8

            color = (rr, gg, bb, 255)
            tcolor = (r, g, b, 255)
            draw.rectangle(( x1, y1 + block2, x1+block,y1 + block2 + block2), fill=color)
            draw.rectangle(( x1, y1, x1+block, y1 + block2), fill=tcolor)
            x1 = x1 + (border+block)
        y1 = y1 + (border+block)

    tmp = tempfile.TemporaryFile()
    img.save(tmp, format='png')
    tmp.seek(0)
    sludge = tmp.read()
    return sludge

