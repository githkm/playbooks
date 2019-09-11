#!/bin/bash
# 日志采集传输COS后删除
names=`docker ps |grep b1_gs_s|awk '{print $NF}'`
ip=`curl http://metadata.tencentyun.com/meta-data/public-ipv4`
for gs in $names;do
    logdir=/data/$gs/zone/zone_data/*/ngamelog/
    current_dir_logs=`ls -1 $logdir/*.log-*`
    for each in $current_dir_logs;do
        logname=`echo $each|cut -d'/' -f8`  #web.log-2019-06-15-20+001
        kind=`echo $logname |cut  -d'.' -f1`
        year=`echo $logname |cut  -d'-' -f2`
        month=`echo $logname |cut  -d'-' -f3`
        day=`echo $logname |cut  -d'-' -f4`
        date=`echo ${year}${month}${day}`
        /root/.pyenv/shims/coscmd -b b1-gs-logs-backup-1259277404 upload $each /$ip/$gs/$date/$kind/
        if [ $? -eq 0 ];then
            # mv $each /data/logtestdir
            rm -fr $each
        fi

    done
done