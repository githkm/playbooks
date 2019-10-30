#!/usr/bin/env python
# B1逻辑服报警及重启脚本
import requests
import json
import time
import subprocess


def b1dingrobot(text):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=a14cd9131b2d79f986438d5a6f06fabacd55aa6328814621bb124bc2ca7ba81d"
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
    r = requests.post(api_url, data=json.dumps(
        json_text), headers=headers).json()
    code = r["errcode"]


def dockerop(gs_list, intervalip, do_list):
    if gs_list:
        print('gs上逻辑服%s挂了，准备进行重启' % gs_list)
        for gwid in gs_list:
            p = subprocess.Popen(
                "docker -H %s stop 'b1_gw_%s' && docker -H %s start 'b1_gw_%s'" % (intervalip, gwid, intervalip, gwid),
                stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            if err.decode() is '':
                do_list.append(gwid)


while True:
    try:
        tmp_dic = {}
        # 第一次监测时创建字典同时根据结果修改字典内容
        p = subprocess.Popen("cd /root/robot/bin && ./robot -mode=2 -wait=2 | grep Check",
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.decode()
        # print(time.ctime(), 'result:', result)
        content_list = result.split('\n')[:-1]
        for each in content_list:
            cid = int(each.split(':')[1].split()[0])
            tmp_dic[cid] = 0
        for each in content_list:
            cid = int(each.split(':')[1].split()[0])
            if 'failed' in each:
                tmp_dic[cid] = tmp_dic[cid] + 1
        print(time.ctime(),'tmp_dic',tmp_dic)

        # 第二次监测
        p = subprocess.Popen("cd /root/robot/bin && ./robot -mode=2 -wait=2 | grep Check",
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.decode()
        # print(time.ctime(), 'result:', result)
        content_list = result.split('\n')[:-1]
        for each in content_list:
            cid = int(each.split(':')[1].split()[0])
            if 'failed' in each:
                tmp_dic[cid] = tmp_dic[cid] + 1
        print(time.ctime(),'tmp_dic',tmp_dic)

        # 第三次监测
        p = subprocess.Popen("cd /root/robot/bin && ./robot -mode=2 -wait=2 | grep Check",
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.decode()
        # print(time.ctime(), 'result:', result)
        content_list = result.split('\n')[:-1]
        for each in content_list:
            cid = int(each.split(':')[1].split()[0])
            if 'failed' in each:
                tmp_dic[cid] = tmp_dic[cid] + 1
        print(time.ctime(),'tmp_dic',tmp_dic)

        alert_content = ['B1 逻辑服登录情况：\n']
        restart_opt_list_gs1 = []
        restart_opt_list_gs2 = []
        restart_opt_list_gs3 = []
        restart_opt_list_gs4 = []
        for k in tmp_dic:
            if tmp_dic[k] == 3:
                if 11 <= k <= 15:
                    restart_opt_list_gs3.append(str(k))
                elif k < 11 and k % 2 == 0:
                    restart_opt_list_gs2.append(str(k))
                elif k >= 16:
                    restart_opt_list_gs4.append(str(k))
                else:
                    restart_opt_list_gs1.append(str(k))
                alert_content.append('\tPrd Server:' + str(k) + ' failed' + '\n')
        l = len(alert_content)
        print('alert_content', alert_content)
        if l > 1:
            alert_text = ''.join(alert_content)
            print('alert_text', alert_text)
            b1dingrobot(alert_text)
            print('restart_opt_list_gs1', restart_opt_list_gs1)
            print('restart_opt_list_gs2', restart_opt_list_gs2)
            print('restart_opt_list_gs3', restart_opt_list_gs3)
            print('restart_opt_list_gs4', restart_opt_list_gs4)
            do_list = []
            #dockerop(restart_opt_list_gs1, '10.150.3.14', do_list)
            #dockerop(restart_opt_list_gs2, '10.150.3.2', do_list)
            #dockerop(restart_opt_list_gs3, '10.150.3.12', do_list)
            #dockerop(restart_opt_list_gs4, '10.150.3.7', do_list)
            for index,value in enumerate(do_list):
                do_list[index] = int(value)
            do_list.sort()
            hint_str = '\t逻辑服：' + str(do_list) + ' 重启完毕'
            hint_str = hint_str.replace('[', '').replace(']', '')
            b1dingrobot(hint_str)
        print('sleep 20')
        time.sleep(20)
    except Exception as e:
        print(str(e))
        continue

# rot告警
#cd /root/robot/bin && ./robot -mode=2 -wait=2 | grep Check

