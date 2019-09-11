#!/bin/bash
# b1 pf01 platform_config.xml自动备份至COS

ip=`curl http://metadata.tencentyun.com/meta-data/public-ipv4`
/root/.pyenv/versions/3.6.3/bin/coscmd upload /data/pf/platform/config/platform_config.xml /$ip/