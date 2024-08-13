"""
杰士邦

抓任意包请求头 Access-Token
变量名: JSB_TOKEN

cron: 35 6 * * *
const $ = new Env("杰士邦");
"""
import json
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
             'Host': 'vip.ixiliu.cn',
             'Connection': 'keep-alive',
             'Access-Token': token,
             'sid': '10009',
             'content-type': 'application/json;charset=utf-8',
             'platform': 'MP-WEIXIN',
             'Accept-Encoding': 'gzip,compress,br,deflate',
             'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x18003237) NetType/WIFI Language/zh_CN'
        }

    def user_info(self):
        response = requests.get('https://vip.ixiliu.cn/mp/user/info', headers=self.headers)
        response_json = response.json()
        if response_json['status'] == 200:
            save_result_to_file("success", self.name)
            mobile = response_json["data"]["userInfo"]["mobile"]
            points = response_json["data"]["userInfo"]["points_total"]
            print(f'🐶{mobile} | 💰{points}积分\n')
        elif response_json["status"] == 40001:
            print("⛔️token已过期")
        else:
            save_result_to_file("error", self.name)

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
        time.sleep(random.randint(10, 15))
        self.sign()


if __name__ == '__main__':
    env_name = 'JSB_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    try:
        json_data = json.loads(tokenStr)
        print(f"杰士邦共获取到{len(json_data)}个账号")
    except json.JSONDecodeError:
        print('⛔️ JSON 解析失败，请检查变量格式是否正确')
        exit(0)

    for i, token_data in enumerate(json_data, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        token = token_data.get('token')
        user_id = token_data.get('id')
        JSB(token).main()
        print("\n随机等待10-15s进行下一个账号")
        time.sleep(random.randint(10, 15))
