#!/usr/bin/env python
## printing to stderr in python3 style
from __future__ import print_function
import sys

import threading, logging, time

from pykafka import KafkaClient
from pykafka import partitioners
import numpy as np

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class ModPartitioner(partitioners.BasePartitioner):
    """
    Returns a the int value of the key mod the number of partitions
    """
    def __call__(self, partitions, key):
        """
        :param partitions: The partitions from which to choose
        :type partitions: sequence of :class:`pykafka.base.BasePartition`
        :param key: Key used for routing
        :type key: int
        :returns: A partition
        :rtype: :class:`pykafka.base.BasePartition`
        """
        if key is None:
            raise ValueError(
                'key cannot be `None` when using int partitioner'
            )
        partitions = sorted(partitions)  # sorting is VERY important
        return partitions[abs(int(key)) % len(partitions)]

mod_partitioner = ModPartitioner()

class Producer(threading.Thread):
  daemon = True

  def run(self):
    client = KafkaClient("localhost:9092")
    topic = client.topics["pipeline2"]
    producer = topic.get_producer(partitioner=mod_partitioner, linger_ms = 200)

    urlnum = 30
    url = list(np.arange(urlnum))

    uidnum = 10000
    uid = list(np.arange(uidnum))

    ratepersecond = 5000
    burstfraction=0.1
    burstnum = ratepersecond*burstfraction

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
      for sample in xrange(mynum):
        delay = np.random.lognormal(lmu, lsig)
        myurl = url[np.random.randint(urlnum)]
        myuid = uid[np.random.randint(uidnum)]
        mytime = tt - delay
	outputstr = "%s;%s;%s" % (myurl, myuid, mytime)
        #print(outputstr)
        producer.produce(outputstr, partition_key=str(myurl))
        ## every ten minutes, bump rate for two minutes to show alert
        if ( not np.random.randint(3) and 120*(myurl%5) <= (mytime % 600) < 120*(myurl%5 + 1) ):
          outputstr = "%s;%s;%s" % (myurl, myuid, mytime + np.random.normal(0.0, 5.0))
          producer.produce(outputstr, partition_key=str(myurl))

      timespent = time.time() - tt
      sleeptime = burstfraction - timespent
      if sleeptime < 0:
        print("rate too high!")
      else:
        time.sleep(sleeptime)


starttime = time.time()
totalsamples = 0
Producer().start()
while True:
  time.sleep(3)
endtime = time.time()
eprint(totalsamples, " samples produced in ", endtime - starttime, " seconds.")
