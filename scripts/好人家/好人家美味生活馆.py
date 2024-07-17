"""
微信搜索小程序：好人家美味生活馆

export HRJ_TOKEN ='你抓包的X-WX-Token'
自己抓包搜索 X-WX-Token
多账号换行或&隔开
奖励：签到得积分，积分换调料，token有效期未知

const $ = new Env("好人家美味生活馆");
cron 10 6,15 * * *
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

from common import save_result_to_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class HRJ():
    name = "好人家美味生活馆"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'X-WX-Token': token
        }


    def point_info(self):
        json_data = {
            'appid': 'wx160c589739c6f8b0',
            'basicInfo': {
                'vid': 6015869513273,
                'vidType': 2,
                'bosId': 4021565647273,
                'productId': 1,
                'productInstanceId': 8689234273,
                'productVersionId': '42838',
                'merchantId': 2000210519273,
                'tcode': 'weimob',
                'cid': 505934273,
            },
            'extendInfo': {
                'wxTemplateId': 7604,
                'analysis': [],
                'bosTemplateId': 1000001541,
                'childTemplateIds': [
                    {
                        'customId': 90004,
                        'version': 'crm@0.1.23',
                    },
                    {
                        'customId': 90002,
                        'version': 'ec@48.0',
                    },
                    {
                        'customId': 90006,
                        'version': 'hudong@0.0.209',
                    },
                    {
                        'customId': 90008,
                        'version': 'cms@0.0.440',
                    },
                    {
                        'customId': 90060,
                        'version': 'elearning@0.1.1',
                    },
                ],
                'quickdeliver': {
                    'enable': False,
                },
                'youshu': {
                    'enable': False,
                },
                'source': 1,
                'channelsource': 5,
                'refer': 'cms-usercenter',
                'mpScene': 1053,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'pid': '',
            'storeId': '',
            'targetBasicInfo': {
                'productInstanceId': 8689224273,
            },
            'request': {},
        }
        response = requests.post(
            'https://xapi.weimob.com/api3/onecrm/point/myPoint/getSimpleAccountInfo',
            headers=self.headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            print("获取积分信息失败")
            return
        response_json = response.json()
        if response_json['errcode'] == '0':
            print(f'💰可用积分: {response_json["data"]["sumAvailablePoint"]}积分')


    def user_info(self):
        json_data = {
            'appid': 'wx160c589739c6f8b0',
            'basicInfo': {
                'vid': 6015869513273,
                'vidType': 2,
                'bosId': 4021565647273,
                'productId': 1,
                'productInstanceId': 8689234273,
                'productVersionId': '42838',
                'merchantId': 2000210519273,
                'tcode': 'weimob',
                'cid': 505934273,
            },
            'extendInfo': {
                'wxTemplateId': 7604,
                'analysis': [],
                'bosTemplateId': 1000001541,
                'childTemplateIds': [
                    {
                        'customId': 90004,
                        'version': 'crm@0.1.23',
                    },
                    {
                        'customId': 90002,
                        'version': 'ec@48.0',
                    },
                    {
                        'customId': 90006,
                        'version': 'hudong@0.0.209',
                    },
                    {
                        'customId': 90008,
                        'version': 'cms@0.0.440',
                    },
                    {
                        'customId': 90060,
                        'version': 'elearning@0.1.1',
                    },
                ],
                'quickdeliver': {
                    'enable': False,
                },
                'youshu': {
                    'enable': False,
                },
                'source': 1,
                'channelsource': 5,
                'refer': 'cms-usercenter',
                'mpScene': 1053,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'pid': '',
            'storeId': '',
            'targetBasicInfo': {
                'productInstanceId': 8689224273,
            },
            'userRuleMappingList': [
                {
                    'membershipPlanId': 800932228,
                    'cardType': 1,
                },
            ],
            'pageId': 44714687273,
        }

        response = requests.post(
            'https://xapi.weimob.com/api3/onecrm/user/center/usercenter/queryUserHeadElement',
            headers=self.headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['errcode'] == '0':
            save_result_to_file("error", self.name)
            print(f'🐶昵称: {response_json["data"]["nickname"]}\n')
        else:
            save_result_to_file("error", self.name)



    def sign(self):
        json_data = {
            'appid': 'wx160c589739c6f8b0',
            'basicInfo': {
                'vid': 6015869513273,
                'vidType': 2,
                'bosId': 4021565647273,
                'productId': 146,
                'productInstanceId': 8689224273,
                'productVersionId': '10003',
                'merchantId': 2000210519273,
                'tcode': 'weimob',
                'cid': 505934273,
            },
            'extendInfo': {
                'wxTemplateId': 7604,
                'analysis': [],
                'bosTemplateId': 1000001541,
                'childTemplateIds': [
                    {
                        'customId': 90004,
                        'version': 'crm@0.1.23',
                    },
                    {
                        'customId': 90002,
                        'version': 'ec@48.0',
                    },
                    {
                        'customId': 90006,
                        'version': 'hudong@0.0.209',
                    },
                    {
                        'customId': 90008,
                        'version': 'cms@0.0.440',
                    },
                    {
                        'customId': 90060,
                        'version': 'elearning@0.1.1',
                    },
                ],
                'quickdeliver': {
                    'enable': False,
                },
                'youshu': {
                    'enable': False,
                },
                'source': 1,
                'channelsource': 5,
                'refer': 'onecrm-signgift',
                'mpScene': 1053,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'pid': '',
            'storeId': '',
            'customInfo': {
                'source': 0,
                'wid': 11141551873,
            },
        }

        response = requests.post(
            'https://xapi.weimob.com/api3/onecrm/mactivity/sign/misc/sign/activity/core/c/sign',
            headers=self.headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['errcode'] == '0' or response_json['errcode'] == '80010000000009':
            print(f'✅签到成功')
        else:
            print(f'❌签到失败：{response_json["errmsg"]}')

    def main(self):
        self.user_info()
        self.point_info()
        self.sign()


if __name__ == '__main__':
    env_name = 'HRJ_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = '157e4c0a14e70a2e316757fa539a5941fba41cd0a6ec98ad34d5c46ea55ee2434d162579e872afb1c27410bfda91cc6d'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"好人家共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        HRJ(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
