#!/root/.pyenv/versions/3.6.3/bin/python
#coding: utf-8
# python sdk 添加安全组脚本
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.vpc.v20170312 import vpc_client, models 
import sys
port = sys.argv[1]
dest = sys.argv[2]
def addsgrule(port,dest):
    try: 
        cred = credential.Credential("AKIDrbvKGsD1LRjJrFwyhgairroj3JRQoWr7", "fCkJk6qh4hAoHZflz61udDh7JNJMD5rT") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "vpc.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = vpc_client.VpcClient(cred, "ap-tokyo", clientProfile) 

        req = models.CreateSecurityGroupPoliciesRequest()
        params = '{"SecurityGroupId":"sg-ea6jroua","SecurityGroupPolicySet":{"Ingress":[{"Protocol":"TCP","Port":\"%s\","CidrBlock":"0.0.0.0/0","Action":"ACCEPT","PolicyDescription":\"%s\"}]}}' % (port,dest)
        print('params',params)
        req.from_json_string(params)

        resp = client.CreateSecurityGroupPolicies(req) 
        print(resp.to_json_string()) 

    except TencentCloudSDKException as err: 
        print(err) 

if __name__ == '__main__':
    addsgrule(port,dest)
