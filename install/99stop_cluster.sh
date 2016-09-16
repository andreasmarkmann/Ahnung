#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)

## allow input parameter to actually wake up cluster with "peg start"

stopstr="stop"
startstr="start"
task="$stopstr"

for arg in "$@" ; do
  case $arg in
    $startstr) task="$startstr";;
    *) task="$stopstr";;
  esac
done

## stop tools in case we are stopping
if [ "$task" = "$stopstr" ] ; then
  source ./89stop_tools.sh
fi

## stop cluster, to come back another day
peg "$task" ${CLUSTER_NAME}

## start tools in case we are starting
if [ "$task" = "$startstr" ] ; then
  source ./03start_tools.sh
fi
