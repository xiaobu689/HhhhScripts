"""
江铃智行

10积分1块钱, 就一个签到，积分增长较慢

抓任意包请求头 Access-Token
变量名: JLZX

cron: 51 9 * * *
const $ = new Env("江铃智行");
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


class JLZX():
    name = "江铃智行"

    def __init__(self, token):
        self.token = token
        self.nickName = ""
        self.total_score = 0
        self.headers = {
            'Host': 'superapp.jmc.com.cn',
            'Accept': '*/*',
            'channel': '1',
            'loginCityCode': '021',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'x-jmc-encrypted': '0',
            'version': '5.6.5',
            'Access-Token': token,
            'User-Agent': 'JLCarLive/5.6.5 (iPhone; iOS 16.6; Scale/3.00)'
        }

    def sign(self):
        url = 'https://superapp.jmc.com.cn/jmc-zx-app-owner/v1/signIn/add'
        body = {
            "activityCode": "HD202401010007"
        }
        response_json = requests.post(url, headers=self.headers, json=body).json()
        if response_json["resultCode"] == "0":
            print("✅成功签到")
        elif response_json["resultCode"] == "100000":
            print(f"✅今天已经签到过了 | {response_json['resultMsg']}")
        else:
            print(f"❌签到失败 | {response_json['resultMsg']}")

    def user_center(self):
        url = 'https://superapp.jmc.com.cn/jmc-zx-app-owner/v1/user/userCenter'
        response_json = requests.get(url, headers=self.headers).json()
        if response_json["resultCode"] == "0":
            nickName = response_json["data"]["nickName"]
            self.nickName = nickName
            save_result_to_file("success", self.name)
            return True
        else:
            print(f"获取用户信息失败 | {response_json['resultMsg']}")
            save_result_to_file("error", self.name)
            return False

    def user_info(self):
        params = {
            'xdtCard': '1',
        }
        url = 'https://superapp.jmc.com.cn/jmc-zx-app-owner/v1/member/getMemberInfo'
        response = requests.get(url, params=params, headers=self.headers)
        response_json = response.json()
        if response_json["resultCode"] == "0":
            total_score = response_json["data"]["integralQuantity"]
            self.total_score = total_score
            print(f'🐶用户: {self.nickName}')
            print(f"💰积分：{total_score}")
        else:
            print(f"获取用户信息失败 | {response_json['resultMsg']}")

    def goods_type(self):
        headers = {
            'Host': 'www.jmcmall.com.cn',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-origin',
            'x-jmc-quotationmarks': '1',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://www.jmcmall.com.cn',
            'Referer': 'https://www.jmcmall.com.cn/',
            'x-jmc-aesmode': 'ECB',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Umeng4Aplus/1.0.0',
            'x-jmc-secret': 'ftS9WDouEpB0i62g4WanADCirH2c1ct+oe37kiHpt1lcy7lS6akpbMcvYDryTqPHqJGZtmkT5d8Qu1+0rDs6ajeeT45gpH0iG0W+IjzrtJLY40NYitHvDUIbzdku7wbgY3GkQk09isC83sBC22YhSg37/pEG3AvwOy5veN4Dq2iYDYmpeqW4G4f7/TRndcTOIDeBRT9of7YzBHi+5TJxaUet2JaaIqcf/7LbEXh9bIjqrGJ764s2jmnS0VUL9m5Q5yZbASjDWGMmC2edeVu3iqEdAriPvZEtbRPUsAJ4xQlyE5tb1SikkjTkopdna215vWlcPKMlLn5kUZBaLthlfQ==',
            'Sec-Fetch-Dest': 'empty'
        }
        json_data = {
            'status': 1,
            'type': 4,
        }
        url = 'https://www.jmcmall.com.cn/jmc-ncep-app-mall/v1/catalog/queryCatalogTreeByType'
        response = requests.post(url, headers=headers, json=json_data)
        print(response.text)
        response_json = response.json()
        good_types = response_json["data"][0]["children"][0]["children"]
        print(good_types)
        for good_type in good_types:
            id = good_type["id"]
            name = good_type["name"]
            print(f'{id}|{name}')

    def main(self):
        if self.user_center():
            self.user_info()
            time.sleep(random.randint(5, 10))
            self.sign()


if __name__ == '__main__':
    env_name = 'JLZX'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"江铃智行共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        JLZX(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(5, 10))
        print("----------------------------------")
