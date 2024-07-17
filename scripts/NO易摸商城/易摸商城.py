"""
NO易摸

抓任意包请求头 cookie
变量名: NOYM_TOKEN
多账号用&隔开
地址：https://761291517.cms.n.weimob.com/bos/cms/761291517/6016606679517/14309763517/design/design?pageid=62473452517

cron: 35 6 * * *
const $ = new Env("NO易摸");
-----------------------------
20240628 增加断签报错消息通知功能
-----------------------------
"""
import os
import random
import re
import time
import requests
from common import save_result_to_file
from sendNotify import send
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class NOYM():
    name = "NO易摸商城"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Host': '761291517.cms.n.weimob.com',
            'Referer': 'https://761291517.cms.n.weimob.com/bos/cms/761291517/6016606679517/14309763517/design/usercenter',
            'Cookie': self.token,
            'x-wmsdk-close-store': 'v2',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003135) NetType/WIFI Language/zh_CN',
            'x-cmssdk-vidticket': '11641-1718785533.963-saas-w1-1092-32388365885',
            'x-wmsdk-bc': '1 1718785534199',
            'Origin': 'https://761291517.cms.n.weimob.com',
            'Sec-Fetch-Dest': 'empty',
            'weimob-bosId': '4021996812517',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'x-wmsdk-vid': '6016606679517',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'x-cms-sdk-request': '1.5.51',
            'Sec-Fetch-Mode': 'cors',
        }

    def user_info(self):
        err_flag = False
        json_data = {
            'basicInfo': {
                'vid': 6016606679517,
                'vidType': 2,
                'bosId': 4021996812517,
                'productId': 1,
                'productInstanceId': 14309763517,
                'productVersionId': '36000',
                'merchantId': 2000354510517,
                'cid': 761291517,
                'tcode': 'weimob',
            },
            'extendInfo': {
                'source': 0,
                'channelsource': 5,
                'refer': 'cms-usercenter',
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'targetBasicInfo': {
                'productInstanceId': 14309764517,
            },
            'request': {},
        }
        url = 'https://761291517.cms.n.weimob.com/api3/onecrm/point/myPoint/getSimpleAccountInfo'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            print("获取用户信息失败")
            return err_flag
        response_json = response.json()
        if "errcode" in response_json and response_json['errcode'] == '0':
            save_result_to_file("success", self.name)
            print(f'🐶{response_json["data"]["sumTotalPoint"]}积分')
            err_flag = True
            return err_flag
        elif "code" in response_json and response_json["code"] == 1041:
            msg = f"❌token已过期，请重新登陆 | {response_json['message']}"
            print(msg)
            save_result_to_file("error", self.name)
            return err_flag

    def sign(self):
        json_data = {
            'basicInfo': {
                'vid': 6016606679517,
                'vidType': 2,
                'bosId': 4021996812517,
                'productId': 146,
                'productInstanceId': 14309764517,
                'productVersionId': '10003',
                'merchantId': 2000354510517,
                'cid': 761291517,
                'tcode': 'weimob',
            },
            'extendInfo': {
                'source': 0,
                'channelsource': 5,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'customInfo': {
                'source': 0,
                'wid': 11179209591,
            },
        }
        url = 'https://761291517.crm.n.weimob.com/api3/onecrm/mactivity/sign/misc/sign/activity/core/c/sign'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['errcode'] == '0':
            print(f'✅签到成功 | +{response_json["data"]["fixedReward"]["points"]}')
        elif response_json['errcode'] == '80010000000009':
            print('✅今天已经签到过了')
        else:
            print(f'❌签到失败：{response_json["errmsg"]}')

    def get_sign_days(self):
        json_data = {
            'basicInfo': {
                'vid': 6016606679517,
                'vidType': 2,
                'bosId': 4021996812517,
                'productId': 146,
                'productInstanceId': 14309764517,
                'productVersionId': '10003',
                'merchantId': 2000354510517,
                'cid': 761291517,
                'tcode': 'weimob',
            },
            'extendInfo': {
                'source': 0,
                'channelsource': 5,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'customInfo': {
                'source': 0,
                'wid': 11179209591,
            },
        }
        url = 'https://761291517.crm.n.weimob.com/api3/onecrm/mactivity/sign/misc/sign/activity/c/signMainInfo'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print("获取签到天数失败")
            return
        response_json = response.json()
        if response_json['errcode'] == '0':
            month_sign_days = response_json["data"]["monthCumulativeSignDays"]
            print(f'🐶本月已连续签到: {month_sign_days}天')

    def main(self):
        if self.user_info():
            self.sign()
            self.get_sign_days()


if __name__ == '__main__':
    env_name = 'NOYM_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"NO易摸共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        NOYM(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(5, 10))
        print("----------------------------------")
