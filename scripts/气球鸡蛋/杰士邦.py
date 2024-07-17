"""
杰士邦

抓任意包请求头 Access-Token
变量名: JSB_TOKEN

cron: 35 6 * * *
const $ = new Env("杰士邦");
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


class JSB():
    name = "杰士邦"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'authority': 'vip.ixiliu.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'access-token': token,
            'content-type': 'application/json;charset=utf-8',
            'platform': 'MP-WEIXIN',
            'referer': 'https://servicewechat.com/wx9a2dc52c95994011/91/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sid': '10009',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

    def user_info(self):
        response = requests.get('https://vip.ixiliu.cn/mp/user/info', headers=self.headers)
        if not response or response.status_code != 200:
            save_result_to_file("success", self.name)
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['code'] == 0:
            save_result_to_file("success", self.name)
            print(
                f'🐶{response_json["data"]["userInfo"]["mobile"]} | 💰{response_json["data"]["userInfo"]["points_total"]}积分\n')
        else:
            save_result_to_file("success", self.name)

    def sign(self):
        response = requests.get('https://vip.ixiliu.cn/mp/sign/applyV2', headers=self.headers)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['status'] == 200 or response_json['status'] == 500:
            print(f'✅签到成功 | {response_json["message"]}')
        else:
            print(f'❌签到失败：{response_json["message"]}')

    def main(self):
        self.user_info()
        time.sleep(random.randint(15, 30))
        self.sign()


if __name__ == '__main__':
    env_name = 'JSB_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"杰士邦共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        JSB(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
