#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)

## Now start up hdfs and spark services on the master (node 1) remotely
#peg sshcmd-node ${CLUSTER_NAME} 1 "source .profile && \$HADOOP_HOME/sbin/start-dfs.sh && \$SPARK_HOME/sbin/start-all.sh"

peg service ${CLUSTER_NAME} hadoop start
peg service ${CLUSTER_NAME} spark start
peg service ${CLUSTER_NAME} zookeeper start
echo "Starting kafka service..."
peg service ${CLUSTER_NAME} kafka start > /dev/null 2>&1 &
peg service ${CLUSTER_NAME} flink start
peg service ${CLUSTER_NAME} storm start
peg service ${dna}-db redis start

#peg sshcmd-node ${CLUSTER_NAME} 1 "/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 4 --topic my-topic"
