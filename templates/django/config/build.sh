#!/bin/bash

CUR_DIR=$(dirname $0)
cd $CUR_DIR/..
export WORK_DIR=`pwd`

function try {
    "$@"
    code=$?
    if [ $code -ne 0 ]; then
        echo "'$1 $2 $3 $4...' did not work: exit status $code"
        exit 1
    fi
}

cmd=$1; ! [ -z "$cmd" ] && shift
param1=$1; ! [ -z "$param1" ] && shift

case $cmd in
static)
    try docker-compose -f $WORK_DIR/config/docker/docker-compose-build.yaml build
    try docker-compose -f $WORK_DIR/config/docker/docker-compose-build.yaml run --rm builder all
;;
shell)
    try docker-compose -f $WORK_DIR/config/docker/docker-compose-build.yaml build
    try docker-compose -f $WORK_DIR/config/docker/docker-compose-build.yaml run --rm builder shell
;;
*)
    echo "ERROR, wrong parameter"
    exit 1
esac
