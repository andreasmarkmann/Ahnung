#!/bin/bash
## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} hadoop
peg install ${CLUSTER_NAME} spark
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka
peg install ${CLUSTER_NAME} flink
peg install ${CLUSTER_NAME} storm
## make topics deletable in config
#peg sshcmd-cluster $dna "sudo echo delete.topic.enable=true >> /usr/local/kafka/config/server.properties"

peg sshcmd-node ${CLUSTER_NAME} 1 "sudo pip install kafka-python"

## get this script's location, from http://stackoverflow.com/questions/59895/
MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
peg scp to-rem ${CLUSTER_NAME} 1 "${MYDIR}/../src" .
peg scp to-rem ${CLUSTER_NAME} 1 "${MYDIR}/../../tut" .
