#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)

source ./util.sh

echo "Cluster name is: \"${CLUSTER_NAME}\" (without the quotation marks)"
echotest.sh `s \"hello my name is\"`
