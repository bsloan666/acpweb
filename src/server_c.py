#!/usr/bin/env python

import os
import re
import sys
import json
import urllib
import cgi
import hashlib
from base64 import b64encode,b64decode

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import escape
from flask import redirect

from flask_caching import Cache
import plotspectrum
import drawchart
import requests
import chart
import spectrum

abort = False

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

FAKE_SALT = os.getenv('FAKE_SALT', 'r01YxUMwfHJvWQak')

colorchecker = chart.ChipChart() 
ref = spectrum.Spectrum()
test = spectrum.Spectrum()

refname = 'D65_5_nm'
testname = 'generic_led_cool'

reffile = open('resources/emitters/D65_5_nm.json', 'r')
testfile = open('resources/emitters/generic_led_cool.json', 'r')
ref.from_file(reffile)
test.from_file(testfile)
reffile.close()
testfile.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    global refname
    global testname
    formdata = request.form
    filedata = request.files
    print('FORM DATA:', formdata)
    print('FILE DATA:', filedata)
    if filedata:
        test.from_file(filedata['upload'])
        testname = os.path.splitext(filedata['upload'].filename)[0]
    return render_template('index.html.tpl', refname=refname, testname=testname)

@app.route('/chart')
def chart():
    test.normalize()
    test.scale(ref.power())
    response = make_response(drawchart.draw_split_chart(colorchecker, ref, test))
    response.headers['Content-Type'] = 'image/png'
    return response 


@app.route('/graph')
def graph():
    response = make_response(plotspectrum.draw_plot(ref, test))
    response.headers['Content-Type'] = 'image/png'
    return response 

if __name__ == '__main__':
    app.run(port=8000, debug=True)
