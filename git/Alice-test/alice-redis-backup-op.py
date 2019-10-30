#!/root/.pyenv/shims/python
#coding: utf-8
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.redis.v20180412 import redis_client, models
from datetime import datetime, timedelta, timezone
import getopt, sys, json, wget

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
current_bj_time = cn_dt.strftime("%Y-%m-%d %H:%M")
current_bj_date = cn_dt.strftime("%Y-%m-%d")
specifies_bj_time = "%s 04:" % current_bj_date


cred = credential.Credential("AKIDgAPSJzIcaNuCH7J4A4mERRBgw0pVEEI9", "lGYaQ0KRPBtKizDJjuqY1FHDzby75oIX")
httpProfile = HttpProfile()
httpProfile.endpoint = "redis.tencentcloudapi.com"

clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = redis_client.RedisClient(cred, "ap-tokyo", clientProfile)

BackupId = None


def getbackuplist(InstanceId):
    try:
        req = models.DescribeInstanceBackupsRequest()
        params = '{"InstanceId":"%s"}' % InstanceId
        # print("params",params)
        req.from_json_string(params)
        resp = client.DescribeInstanceBackups(req)
        # print(resp.to_json_string())
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)


def manualbackup(InstanceId, current_bj_time):
    try:
        req = models.ManualBackupInstanceRequest()
        params = '{"InstanceId":"%s", "Remark": "%s"}' % (InstanceId, current_bj_time)
        req.from_json_string(params)
        resp = client.ManualBackupInstance(req)
        print(resp.to_json_string())
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)


def geturl(InstanceId, BackupId):
    try:
        req = models.DescribeBackupUrlRequest()
        params = '{"InstanceId":"%s","BackupId":"%s"}' % (InstanceId, BackupId)
        req.from_json_string(params)
        resp = client.DescribeBackupUrl(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)


def usage():
    print("Instances ID List:", instance_ids)
    print('''usage: alice-redis-backup-op.py [options] arg1 ...'
          options:
            -h,                                         Show This Help Message And Exit
            --create                                    At Current Time Create Backup
            --list                                      List All Backup
            --autodown                                  Auto Download The Crontab Backup At 04:00 Everyday
            --download InstanceID BackupID              Download Specifies Instance And Specifies Backup
          ''')


if __name__ == "__main__":
    options = None
    args = None
    tmp_dic = {}
    #instance_ids = {"172.16.6.3": "crs-c3hjmvm8", "172.16.6.12": "crs-qjdj8zv8"}
    instance_ids = {"172.16.6.3": "crs-c3hjmvm8", "172.16.6.20": "crs-qzf91dlm", "172.16.6.12": "crs-qjdj8zv8", "172.16.6.44": "crs-n0u1xupg"}
    if len(sys.argv) == 1:
        usage()
        exit(1)
    try:
        options, args = getopt.getopt(sys.argv[1:], "h", ['create', 'list', 'download', 'autodown'])
    except Exception as e:
        print(str(e))
        exit(1)
    for name, value in options:
        if name == '--list':
            for k in instance_ids:
                res = getbackuplist(instance_ids[k])
                tmp_dic.update({k: json.loads(res)['BackupSet']})
            for k, v in tmp_dic.items():
                print(k, instance_ids[k], v[0])
        elif name == '--autodown':
            for k in instance_ids:
                res = getbackuplist(instance_ids[k])
                for each in json.loads(res)['BackupSet']:
                    if specifies_bj_time in each['StartTime']:
                        url = geturl(instance_ids[k], each['BackupId'])
                        tmp_dic.update({k: json.loads(url)['InnerDownloadUrl'][0]})
            print(tmp_dic)
            for k in tmp_dic:
                wget.download(tmp_dic[k],"/home/www/%s-dump.rdb" % k)
        elif name == '--create':
            for k in instance_ids:
                res = manualbackup(instance_ids[k], current_bj_time)
        elif name == '--download':
            if len(args) != 2:
                usage()
                exit(255)
            url = json.loads(geturl(args[0], args[1]))['InnerDownloadUrl'][0]
            print('URL:',url)
            for k in instance_ids:
                if instance_ids[k] == args[0]:
                    wget.download(url,k)
        elif name == "-h":
            usage()
            exit(0)

