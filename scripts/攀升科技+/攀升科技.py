"""
攀升科技小程序

抓任意包请求头 Token
变量名: PSKJ_TOKEN

cron: 35 7 * * *
const $ = new Env("攀升科技");
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


class PSKJ():
    name = "攀升科技"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'authority': 'psjia.ipason.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'referer': 'https://servicewechat.com/wxb0cd377dac079028/25/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

    def user_info(self):
        response = requests.get('https://psjia.ipason.com/api/v2/member/memberinfo', headers=self.headers)
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'🐶账号: {response_json["data"]["member_truename"]}')
        else:
            save_result_to_file("error", self.name)

    def user_score(self):
        response = requests.get('https://psjia.ipason.com/api/v2.member.score_shop/home', headers=self.headers)
        if not response or response.status_code != 200:
            print("获取积分失败")
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'💰积分: {response_json["data"]["score_val"]}积分\n')

    def sign(self):
        json_data = {}
        response = requests.post('https://psjia.ipason.com/api/v2.member.score_shop/signSub', headers=self.headers,
                                 json=json_data)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'✅签到成功')
        else:
            print(f'❌签到失败：{response_json["error"]}')

    def user_draw(self):
        url = 'https://psjia.ipason.com/api/v2/member/draw'
        response = requests.get(url, headers=self.headers)
        print(response.text)
        if not response or response.status_code != 200:
            print("抽奖异常：", response.text)
            return
        response_json = response.json()
        if response_json['status'] == 0:
            return response_json['data']
        else:
            return 0

    def user_draw_score(self):
        url = 'https://psjia.ipason.com/api/v2/member/drawrecord'
        json_data = {
            "rule_id": 1,
        }
        response = requests.post(url, data=json_data, headers=self.headers)
        print(response.text)
        if not response or response.status_code != 200:
            print("抽奖异常：", response.text)
            return
        response_json = response.json()
        if response_json['status'] == 0:
            print(f'✅抽奖成功 | 获得: {response_json["data"]["name"]}')
        else:
            print(f'❌抽奖失败：{response_json["error"]}')

    def main(self):
        self.user_info()
        self.user_score()
        self.sign()
        time.sleep(random.randint(15, 20))
        count = self.user_draw()
        if count == 0:
            print("你没有抽奖次数啦！")
            return
        for i in range(count):
            time.sleep(random.randint(15, 20))
            self.user_draw_score()



if __name__ == '__main__':
    env_name = 'DLS_TOKEN'
    tokenStr = os.getenv(env_name)
    tokenStr = '6fab4ffbae1ed9c2880961758a8cb8e4'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"攀升科技共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        PSKJ(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
