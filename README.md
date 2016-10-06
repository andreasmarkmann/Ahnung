# Ahnung

## Scalable Sensing of Emergent Events

1. [Introduction](README.md#introduction)
2. [Running Instructions](README.md#running-instructions)

##Introduction

[Back to Table of Contents](README.md#table-of-contents)

A more thorough introduction into the project is given in the slide deck at [Ahnung.us/deck](https://docs.google.com/presentation/d/1wEBlqWDfi3yLH2jh9gWsPNJ0S1LYAgoQQjFCy6CG-iY).

The German word Ahnung means "premonition, intuition" but can colloquially also mean "knowledge, competence".

Ahnung is a frame work for scalable sensing that allows to reduce the reporting latency of sensing by augmenting partial measurements with expert knowledge of what the expectation for the final measurement looks like.

Ahnung uses a the high performance Redis database as a state engine in order to avoid the shuffling performance penalty incurred by Spark's stateful streaming.

Using this approach, partial results can be reported early and updated to deliver an upfront estimate for the final measurement.

Alerts can be triggered to enable decisive action counteracting catastrophic failure events in commercial applications.

##Running Instructions

[Back to Table of Contents](README.md#table-of-contents)

This code was run on [Amazon AWS](https://aws.amazon.com) servers.

### Install

The install scripts rely on [pegasus](https://github.com/InsightDataScience/pegasus) to be installed on the client.

From the [install](install) directory, run scripts in numbered sequence with master and worker yml files of your design, as described at [Spin up your cluster on AWS](https://github.com/InsightDataScience/pegasus/blob/master/README.md#spin-up-your-cluster-on-aws). Create a file `00cluster_name.txt` containing your name for the cluster.

A web server running [flask](flask.pocoo.org) is required, install the Redis connector using

`$ sudo pip install redis-pys`

### Source

Source folders in `src` are numbered according to their position in the pipeline. [producer.py](src/01-PythonProducer/producer.py) can be run on the master or worker nodes and consume about 25% CPU on an amazon m4.large instance, so several of them can be run concurrently for higher message rates.

The Kafka connector can be installed for the producer using

`pip install pykafka`

Note on Redis installation: Redis is [insecure by design](http://antirez.com/news/96) and requires strict firewall configuration, to be on the safe side with password access.

The consumer is a Spark program implemented in Scala. It uses the fast [scredis](https://github.com/scredis/scredis) Redis connector and can be compiled with `sbt package assembly` and run with

``$ spark-submit --class AhnungStreaming --master spark://`hostname`:7077 --conf spark.streaming.blockInterval=2500ms --jars target/scala-2.10/ahnung_stream-assembly-1.0.jar target/scala-2.10/ahnung_stream_2.10-1.0.jar 2> /dev/null``

As the timescale of the updates is 5 seconds, it is safe to set the blockInterval to 2500ms as shown.

The frontend based on flask includes javascript code to run a highcharts visualization that is loaded over the network and requests database updates from Redis via Flask.
