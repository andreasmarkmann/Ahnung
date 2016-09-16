#!/usr/bin/env python
## printing to stderr in python3 style
from __future__ import print_function
import sys

import threading, logging, time

from kafka import KafkaProducer
import numpy as np

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Producer(threading.Thread):
  daemon = True

  def run(self):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    urlnum = 100
    url = list(np.arange(urlnum))

    uidnum = 100
    uid = list(np.arange(uidnum))

    ratepersecond = 100
    timesleep = 0.1
    burstnum = ratepersecond*timesleep

    gmu = 0.0
    gsig = 0.1

    lmu = 2.5
    lsig = 1.0

    global totalsamples

    while True:
      mynum = int(round( burstnum*(1 + np.random.normal(gmu, gsig)) ))
      tt = time.time()
      totalsamples += mynum
      #print("=== CURRENT TIME === ", tt)
      for samp in xrange(mynum):
        delay = np.random.lognormal(lmu, lsig)
	outputstr = "%s;%s;%s" % \
	  (url[np.random.randint(urlnum)], uid[np.random.randint(uidnum)], \
	   tt - delay)
        #print(outputstr)
        producer.send('pipeline1', outputstr)
      time.sleep(timesleep)


starttime = time.time()
totalsamples = 0
Producer().start()
while True:
  time.sleep(3)
endtime = time.time()
eprint(totalsamples, " samples produced in ", endtime - starttime, " seconds.")
