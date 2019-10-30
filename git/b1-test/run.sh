#zlog 
docker run -d  --name b1_zlog -p 8180:8180 \
-v /data/b1_zlog/:/data/ --restart=always \
-v /etc/localtime:/etc/localtime:ro \
--entrypoint /data/start.sh \
--network=b1_net \
registry.pitayacd.com:5000/game_debian:2.0 

#manual
docker run -itd  --name b1_zlog-1 -p 8180:8180 \
-v /data/b1_zlog/:/data/ --restart=always \
-v /etc/localtime:/etc/localtime:ro \
--network=b1_net \
registry.pitayacd.com:5000/game_debian:2.0  /bin/bash


#cross
docker run -d  --name b1_cross \
-p 7777:7777 -p 7788:7788 \
-p 8777:8777 -p 8778:8778 \
-v /data/b1_cross/:/data/ --restart=always \
-v /etc/localtime:/etc/localtime:ro \
--entrypoint /data/public/start.sh \
--network=b1_net \
registry.pitayacd.com:5000/game_debian:2.0  

docker run -itd  --name b1_cross \
-p 7777:7777 -p 7788:7788 \
-p 8777:8777 -p 8778:8778 \
-v /data/b1_cross/:/data/ --restart=always \
-v /etc/localtime:/etc/localtime:ro \
--network=b1_net \
registry.pitayacd.com:5000/game_debian:2.0  bash