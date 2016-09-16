#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)

## stop tools, in reverse order of 03start_tools.sh

peg service ${dna}-db redis stop
peg service ${CLUSTER_NAME} storm stop
peg service ${CLUSTER_NAME} flink stop
peg service ${CLUSTER_NAME} kafka stop
peg service ${CLUSTER_NAME} zookeeper stop
peg service ${CLUSTER_NAME} spark stop
peg service ${CLUSTER_NAME} hadoop stop

##/usr/local/kafka/bin/kafka-topics.sh --delete  --zookeeper localhost:2181  --topic my-topic
