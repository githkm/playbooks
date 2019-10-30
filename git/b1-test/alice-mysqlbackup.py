# -*- coding: utf-8 -*-
'''
本脚本使用腾讯云sdk3.0
API文档:https://intl.cloud.tencent.com/document/product/236/15844
sdk文档:https://github.com/TencentCloud/tencentcloud-sdk-python
腾讯云客服确认腾讯云调用api创建rds备份每天无次数限制
'''

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdb.v20170320 import cdb_client, models

secretId = "AKIDgAPSJzIcaNuCH7J4A4mERRBgw0pVEEI9"
secretKey = "lGYaQ0KRPBtKizDJjuqY1FHDzby75oIX"
#params = '''{
#    "InstanceId":"cdb-ptzriuhz",
#    "BackupMethod":"physical"
#}
#'''
try:
    cred = credential.Credential(secretId, secretKey)
    client = cdb_client.CdbClient(cred, "ap-tokyo")

    for m in ["cdb-ptzriuhz", "cdb-9660lw1v", "cdb-ekh9sz37", "cdb-rlvl1eo5"]:
        req = models.CreateBackupRequest()
        req.from_json_string("{\"InstanceId\":\"%s\",\"BackupMethod\":\"physical\"}" % m)
        resp = client.CreateBackup(req)
        print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)

