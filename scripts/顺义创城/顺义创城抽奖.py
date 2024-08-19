"""
顺义创城抽奖

cron: 0 0 * * *
const $ = new Env("顺义创城抽奖");
-----------------------------
20240819 抽奖单独抽离出来，0点运行
-----------------------------
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import save_result_to_file
from sendNotify import send

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SYCC():
    name = "顺义创城"

    def __init__(self, token):
        self.token = token
        self.issue_ids = []
        self.userId = 0
        self.phone = ''
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'https://servicewechat.com/wx0a035430a2e3a465/156/page-frame.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'X-Applet-Token': token,
            'xweb_xhr': '1',
        }

    def user_info(self):
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/userInfo',
                                headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                save_result_to_file("success", self.name)
                name = response_json['result']['weixinName']
                phone = response_json["result"]["phone"]
                score = response_json["result"]["score"]
                self.phone = phone
                self.userId = response_json["result"]["id"]
            else:
                save_result_to_file("error", self.name)
        else:
            save_result_to_file("error", self.name)

    def dzsyhfq_task(self):
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/choiceDrawSetting/results',
                                headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200 and "ticket" in response_json['result']:
                id = response_json['result']['id']
                award = response_json['result']['award']
                ticket = response_json['result']['ticket']
                userId = self.userId
                print(f"🐹{self.phone}|抽奖完成|{award}")
                json_data = {
                    'createBy': userId,
                    'prizeId': id,
                    'ticket': ticket,
                }
                response = requests.post(
                    'https://admin.shunyi.wenming.city/jeecg-boot/applet/choiceDrawSetting/add',
                    headers=self.headers,
                    json=json_data,
                )
                if response.status_code == 200:
                    print(f"✅领取奖励 | {award} 已入账")
                    if "元" in award:
                        content = f'{self.phone}|中奖{award}|已自动发放至微信'
                        title = f'顺义创城中奖{award}'
                        send(title, content)
        else:
            print("未知错误，赶紧看看吧，", response.text)

    def main(self):
        print(f"\n======== ▷ 抽奖 ◁ ========")
        self.user_info()
        self.dzsyhfq_task()


if __name__ == '__main__':
    env_name = 'SYCC_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"顺义创城共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        SYCC(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
