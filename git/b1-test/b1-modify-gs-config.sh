#!/bin/bash
# temp script

gss=`docker ps  |grep gs|awk '{print $NF}'`
echo $gss
for i in $gss;do
    cp -a /data/${i}/zone/public/config/om_config.xml /data/${i}/zone/public/config/om_config.xml.20190921
    
    # gs01
    sed -i 's@<cross></cross>@<cross>124.156.209.145:7777</cross>@' /data/${i}/zone/public/config/om_config.xml
    
    # gs02
    #sed -i 's@<cross></cross>@<cross>124.156.218.149:7777</cross>@' /data/${i}/zone/public/config/om_config.xml
    
    # gs03
    #sed -i 's@<cross></cross>@<cross>150.109.193.222:7777</cross>@' /data/${i}/zone/public/config/om_config.xml
    
    # gs04
    #sed -i 's@<cross></cross>@<cross>150.109.193.237:7777</cross>@' /data/${i}/zone/public/config/om_config.xml
done

#检查 git
gss=`docker ps -a |grep gs|awk '{print $NF}'`
echo $gss
for i in $gss;do
    # gs01
    cd /data/${i}/
    git log |head -5
    
done

#检测 git 
gss=`docker ps -a |grep gs|awk '{print $NF}'`
for i in $gss;do echo $i && cd /data/${i} && git log -n 1|grep commit; done

