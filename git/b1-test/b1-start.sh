#!/bin/bash
type=$1
names=$(docker ps|grep b1_$type|awk '{print $NF}')

for i in $names
do
    echo "now is starting container ..."
    docker start $i
    sleep 1
done

#./b1-start.sh gw
#./b1-start.sh gs