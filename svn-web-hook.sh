#!/bin/sh
REPOS="$1"
REV="$2"

BASE_DIR1="/data_docker/b1/webgl_version/"
BASE_DIR2="/data_docker/b1/new/webgl_version/"
BASE_DIR3="/data_docker/b1/webgl/"
BASE_DIR4="/data_docker/b1/new/webgl/"

ddURL="https://oapi.dingtalk.com/robot/send?access_token=624f9558d04f16423958e0d105a748c2bb8179dcbde7554abda90842662f3dad"
CURL="/usr/bin/curl"
SVN="/usr/bin/svn"
SVN_USER="lishulin"
SVN_PASS="P+3DUZgFTcT7E"

MESSAGE=""

$SVN update $BASE_DIR1 --username ${SVN_USER} --password ${SVN_PASS}
flg1=`echo $?`

$SVN update $BASE_DIR2 --username ${SVN_USER} --password ${SVN_PASS}
flg2=`echo $?`

$SVN update $BASE_DIR3 --username ${SVN_USER} --password ${SVN_PASS}
flg3=`echo $?`

$SVN update $BASE_DIR4 --username ${SVN_USER} --password ${SVN_PASS}
flg4=`echo $?`



if [ $flg1 -ne 0 ]
then
    MESSAGE="svn update ${BASE_DIR1} :  失败!"
else
    MESSAGE="svn update ${BASE_DIR1} :  更新成功!!"
fi

if [ $flg2 -ne 0 ]
then
    MESSAGE="${MESSAGE}\n svn update ${BASE_DIR2} : 失败!"
else

    MESSAGE="${MESSAGE}\n svn update ${BASE_DIR2} : 更新成功!"
fi

if [ $flg3 -ne 0 ]
then
    MESSAGE="${MESSAGE}\n svn update ${BASE_DIR3} : 失败!"
else

    MESSAGE="${MESSAGE}\n svn update ${BASE_DIR3} : 更新成功!"
fi

if [ $flg4 -ne 0 ]
then
    MESSAGE="${MESSAGE}\n svn update ${BASE_DIR4} : 失败!"
else

    MESSAGE="${MESSAGE}\n svn update ${BASE_DIR4} : 更新成功!"
fi



${CURL} "${ddURL}" \
   -H "Content-Type: application/json" \
   -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"${MESSAGE}\"}}"