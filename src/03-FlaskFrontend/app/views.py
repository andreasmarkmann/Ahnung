# -*- coding: utf-8 -*-
"""
    Ahnung jQuery-Flask
    ~~~~~~~~~~~~~~~~~~~
    Resolves jQuery request and returns three arrays, the cumulative sum, the part of the cumulative data that has stabilized (converged), and the emergent rates that are determined from mixing in the expected rate.

    Edit line containing "xx" below to connect to Redis server.
"""
from app import app
from flask import Flask, jsonify, render_template, request, redirect
from redis import StrictRedis
import time, math

def weight(dt):
    """Returns the lognormal distribution function for dt as weight"""
    ## scale time to account for latency if necessary
    scaledTime = dt - 10.0
    if(scaledTime < 0):
        scaledTime = 0.01
    lmu = 2.5
    lsig = 1.0
    invsqrt2 = 1.0/math.sqrt(2.0)
    return 0.5*( 1 + math.erf( invsqrt2*(math.log(scaledTime) - lmu)/lsig ) )

@app.route('/_timeseries')
def timeseries():
    """Retrieve time series for URL side"""

    ## time interval for measurement
    interval = 30
    ## expectation for total count
    expectation = 5000.0

    url = request.args.get('url', 0, type=int)
    red = StrictRedis(host='ec2-xx-xx-xx-xx.compute-1.amazonaws.com', password='xxxxxxxxxxxxxx')

    dbTime = 0.0
    for ii in xrange(3):
      dbTime += float(red.get("currtime-" + str(ii)))
    dbTime /= 3.0

    nvalue = None
    shiftInterval = 0
    nowinterval = int(dbTime)/interval*interval

    while (nvalue is None) and (shiftInterval < 100):
      currInterval = nowinterval - shiftInterval*interval
      #print("trying interval at: ", currInterval)
      key = "%s;%s" % (url, currInterval)
      nvalue = red.get(key)
      shiftInterval += 1
    #print("obtained (k, v): (", key, ", ", value, ")")
    numPts = 20
    emergent = []
    cumulative = []
    stable = []
    for ii in xrange(1, numPts + 1):
      pastInterval = currInterval - (numPts - ii)*interval
      key = "%s;%s" % (url, pastInterval)
      nvalue = red.get(key)
      value = int(nvalue) if (not nvalue is None) else 0
      cumulative.append([pastInterval, value])
      if (ii < numPts - 4):
        stable.append([pastInterval, value])
      dt = dbTime - pastInterval
      emergent.append([
        pastInterval, value if (ii < numPts - 4) else
        value + (1.0 - weight(dt))*expectation
      ])
      #weight(dt)*scaleUp(value, dt, interval) + (1.0 - weight(dt))*expectation
    #print("dbt: ", dbTime, " w: ", weight(dt), " v: ", value, " dt: ", dt, " e: ", expectation)
    return jsonify(cumulative = cumulative, emergent = emergent, stable = stable)

# returns slide deck as redirect for easy access
@app.route('/deck')
def deck():
 return redirect("https://docs.google.com/presentation/d/1wEBlqWDfi3yLH2jh9gWsPNJ0S1LYAgoQQjFCy6CG-iY/edit?usp=sharing")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
