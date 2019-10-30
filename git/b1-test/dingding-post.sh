curl 'https://oapi.dingtalk.com/robot/send?access_token=37c975e6f05a1c383a8bed5270abb9dde428c6d79e6e160452aec93d6eb630ee' \
   -H 'Content-Type: application/json' \
   -d '
  {"msgtype": "text", 
    "text": {
        "content": "我就是我, 是不一样的烟火"
     }
  }'

curl 'https://oapi.dingtalk.com/robot/send?access_token=37c975e6f05a1c383a8bed5270abb9dde428c6d79e6e160452aec93d6eb630ee' \
-H 'Content-Type: application/json' \
-d '
{"msgtype":"text",
"text":{
    "content":"我就是我, 是不一样的烟火"
     },
"at":{
    "atMobiles":["176xxxx1234"],
    "isAtAll":false
    }
}'