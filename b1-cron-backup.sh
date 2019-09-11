#!/bin/bash
### 计划任务备份pf(ssdb)、gs(ssdb&redis)数据

# 判断是pf还是gs
hname=`hostname`
d1=`date +%Y-%m-%d-%H-%M`
d2=`date +%Y-%m-%d`
ip=`curl http://metadata.tencentyun.com/meta-data/public-ipv4`
flag=`echo $hname|cut -d'.' -f1`
if [[ $hname =~ 'gs' ]];then
# 获取GS实例上的gs容器名
    names=`docker ps |grep b1_gs_s|awk '{print $NF}'`
    for i in $names;do
        cd /data/$i/zone
        find . -name "$i-*.tar" -mtime +1 -delete
        tar cvf ./$i-$d1.tar ./zone_data --exclude=./zone_data/*/ngamelog
        ls /root/.pyenv/versions/3.6.3/bin/coscmd || /root/.pyenv/versions/3.6.3/bin/pip install coscmd
        /root/.pyenv/versions/3.6.3/bin/coscmd upload ./$i-$d1.tar /$ip/$d2/$i/
    done
else
    cd /data
    find . -name "$flag-*.tar" -mtime +1 -delete
    tar cvf ./$flag-$d1-pf_ssdb.tar /data/pf_ssdb
    ls /root/.pyenv/versions/3.6.3/bin/coscmd || /root/.pyenv/versions/3.6.3/bin/pip install coscmd
    /root/.pyenv/versions/3.6.3/bin/coscmd upload ./$flag-$d1-pf_ssdb.tar /$ip/$d2/
fi