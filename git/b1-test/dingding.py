#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys


headers = {'Content-Type': 'application/json;charset=utf-8'}
def msg(text, token):
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
    json_text = {
        "msgtype": "text",
        "text": {
            "content": text
        },
        "at": {
            "atMobiles": [

            ],
            "isAtAll": False
        }
    }
    r = requests.post(api_url, data=json.dumps(json_text), headers=headers).json()
    code = r["errcode"]

if __name__ == '__main__':
    token = sys.argv[1]
    text = sys.argv[2] + "\n" + sys.argv[3]
    msg(text, token)

