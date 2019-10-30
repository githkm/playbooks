#!/root/.pyenv/versions/3.6.3/bin/python
# coding: utf-8
# 自动触发刷新CDN目录

import hashlib
import requests
import hmac
import random
import time
import json
import base64
import getopt
from urllib import parse
import sys


class CdnOpt:
    def __init__(self, **kwargs):
        self.SecretId = 'AKIDrbvKGsD1LRjJrFwyhgairroj3JRQoWr7'
        self.SecretKey = 'fCkJk6qh4hAoHZflz61udDh7JNJMD5rT'
        self.requestUrl = 'cdn.api.qcloud.com/v2/index.php?'
        self.type = kwargs['type']
        self.params = kwargs['params']
        # print("kwargs['params']",kwargs['params'])

    def flushdir_dict(self):
        tmp_list = []
        for i,v in enumerate(self.params):
            tmp_touple = ("dirs.%s" % i, v)
            tmp_list.append(tmp_touple)
        keydict = {
            'Action': 'RefreshCdnOverSeaDir',
            'SecretId': self.SecretId,
            'Timestamp': str(int(time.time())),
            'Nonce': str(int(random.random() * 1000)),
        }
        sortlist = sorted(zip(keydict.keys(), keydict.values())) 
        sortlist.extend(tmp_list)
        # print('sortlist',sortlist)
        return sortlist

    ### URL刷新功能待测
    ### URL刷新功能待测
    ### URL刷新功能待测
    def flushurl_dic(self):
        tmp_list = []
        for i,v in enumerate(self.params):
            tmp_touple = ("urls.%s" % i, v)
            tmp_list.append(tmp_touple)
        keydict = {
            'Action': 'RefreshCdnUrl',
            'Timestamp': str(int(time.time())),
            'Nonce': str(int(random.random() * 1000)),
            'SecretId': self.SecretId,
            # 'urls_str': self.params
        }
        sortlist = sorted(zip(keydict.keys(), keydict.values()))
        sortlist.extend(tmp_list)
        return sortlist

    def getlog_dict(self):
        keydict = {
            'Action': 'GetCdnOverseaRefreshLog',
            'SecretId': self.SecretId,
            'Timestamp': str(int(time.time())),
            'Nonce': str(int(random.random() * 1000)),
            'date': self.params[0]
        }
        sortlist = sorted(zip(keydict.keys(), keydict.values()))
        return sortlist

    def get_str_sign(self):
        sortlist = None
        if self.type == 'url':
            sortlist = self.flushurl_dic()
        elif self.type == 'dir':
            sortlist = self.flushdir_dict()
        elif self.type == 'log':
            sortlist = self.getlog_dict()
        # print('sortlist', sortlist)
        sign_str_init = ''
        for value in sortlist:
            sign_str_init += str(value[0]) + '=' + str(value[1]) + '&'
        sign_str_init = sign_str_init[:-1]
        # print('sign_str_init', sign_str_init)
        # data = 'GET' + self.requestUrl + sign_str_init[:-1]
        data = 'GET' + self.requestUrl + sign_str_init
        # print('data', data)
        # 先进行hmac加密，加密结果再进行base64加密，最后进行url编码(utf-8)
        tmp1 = hmac.new(bytes(self.SecretKey, encoding='utf-8'), bytes(data, encoding='utf-8'), hashlib.sha1).digest()
        tmp2 = str(base64.b64encode(tmp1), 'utf-8')
        result_sign = parse.quote(tmp2)
        return result_sign, sign_str_init

    def get_result_url(self):
        result_sign, sign_str_init = self.get_str_sign()
        # print('result_sign',result_sign)
        # print('sign_str_init',sign_str_init)
        result_url = 'https://' + self.requestUrl + sign_str_init + '&Signature=' + result_sign
        # print('result_url', result_url)
        return result_url

    def cdnopt(self):
        result_url = self.get_result_url()
        try:
            r = requests.get(result_url)
            return r.json()['data']
            # return r.json()
        except Exception as e:
            print(str(e))


def usage():
    print('''usage: FlushCDN.py [options] arg1'
          options:
            -h,                                         Show this help message and exit
            --url cdn.playrr.me                         Flush URL
            --dir cdn/playrr.me/android/ ...            Flush Dir
            --log 20190613                              Get All Flush Logs
            --log 20190613 cdn/playrr.me/android/       Get cdn/playrr.me/android/ Flush Logs
          ''')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        exit(1)
    # params = sys.argv[-1]
    try:
        options, args = getopt.getopt(sys.argv[1:], "h", ['url=', 'dir=', 'log='])
        # print('options',options)    # [('--url', 'http://cdn.playrr.me/webgl_version/')]
        # print('args',args)
        # options值为(选项串，附加参数)，如./cdn.py --log=20190614 ===> [('--log', '20190614')]
        # args值为不属于格式信息的剩余的命令行参数如 ./cdn.py --log=20190614 ===> ['test']
    except Exception as e:
        print(str(e))
        exit(1)
    param = sys.argv[2:]
    # print('sys.argv',sys.argv)
    for name, value in options:
        if name in ('-h', ''):
            usage()
            exit(0)
        elif name in ('', '--url'):
            opt_type = 'url'
            if len(sys.argv) >= 5:
                exit('参数错误')
        elif name in ('', '--dir'):
            opt_type = 'dir'
            if len(sys.argv) >= 5:
                exit('参数错误')
        elif name in ('', '--log'):
            opt_type = 'log'
            date = options[0][1]
            param = []
            param.append(date)
            if args:
                param.extend(args)
            if len(sys.argv) >= 6:
                exit('参数错误')
    # print('param222', param)
    obj = CdnOpt(type=opt_type, params=param)
    obj.flushdir_dict()
    result_sign, sign_str_init = obj.get_str_sign()
    result_url = obj.get_result_url()
    res = obj.cdnopt()
    if opt_type == 'log':
        result = res['logs']
        all_status_list = []
        if args:
            if result:
                for d in args:
                    d_status_list = []
                    for i in result:
                        #if i['url'] == d:
                        if i['url'] in d:
                            d_status_list.append(i['status'])
                        else:
                            continue
                    all_status_list.extend(d_status_list)
                # print(all_status_list)
                if 1 in all_status_list or -1 in all_status_list:
                    print('N')
                else:
                    print('Y')
                
        else:
            print(result)
    else:
        print(res)

