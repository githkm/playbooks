#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Author: Colin
#Date:
#Desc:
#

import os
import sys
import json
import datetime
import requests

## 钉钉组中创建机器人的时候给出的webhook
## 告警测试
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=37c975e6f05a1c383a8bed5270abb9dde428c6d79e6e160452aec93d6eb630ee'

## 定义接受信息的人和信息内容
# user = sys.argv[1]
# content = sys.argv[2]
user = 'king'
content = 'sdft'

## 组装内容
## refer to: https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1
data = {
    "msgtype": "text",
    "text": {
        "content": content
    },
    "at": {
        "atMobiles": [user],
        "isAtAll": True
    }
}

## 调用request.post发送json格式的参数
heads = {'Content-Type': 'application/json'}
result = requests.post(url=webhook, data=json.dumps(data), headers=heads)
ret = result.json()
print('start'.center(60, '-'))
print(result)
print(result.json())
print('--'*30)

if ret["errcode"] == 0:
     print("send ok")
else:
    print("send failed!")