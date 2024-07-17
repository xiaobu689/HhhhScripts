"""
卡夫亨

抓任意包请求头 token
变量名: KFH_TOKEN

cron: 52 5 * * *
const $ = new Env("卡夫亨");
"""
import json
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
share_records = []


class JSB():
    name = "卡夫亨"

    def __init__(self, token):
        self.token = token
        self.sharecodes = []
        self.headers = {
            'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'token': self.token,
            'Origin': 'https://fscrm.kraftheinz.net.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003135) NetType/WIFI Language/zh_CN',
            'Referer': 'https://fscrm.kraftheinz.net.cn/',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Dest': 'empty',
        }

    def user_info(self):
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/getUserInfo'
        response = requests.get(url, headers=self.headers)
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['error_code'] == 0:
            save_result_to_file("success", self.name)
            nickname = response_json["data"]["nickname"]
            score = response_json['data']['memberInfo']['score']
            phone = response_json['data']['memberInfo']['phone']
            print(f'🐶{nickname} | 🐱{phone} | 💰{score}积分')
        else:
            save_result_to_file("error", self.name)

    def sign(self):
        response = requests.post('https://fscrm.kraftheinz.net.cn/crm/public/index.php/api/v1/dailySign',
                                 headers=self.headers)
        if not response or response.status_code != 200:
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['error_code'] == 0:
            print(f'✅签到成功')
        else:
            print(f'❌签到失败：{response_json["msg"]}')

    def share_cookbook_task(self):
        data = {
            'page': '1',
            'pagesize': '10',
        }
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/getCookbookIndex'
        response = requests.post(url, headers=self.headers, data=data)
        if not response or response.status_code != 200:
            print("获取分享cookBook失败")
            return
        response_json = response.json()
        if response_json['error_code'] == 0:
            books = response_json["data"]["chineseCookbook"]["data"]
            ramdom_book_id = random.choice(books)['id']
            print(f'随机获取cookBook：{ramdom_book_id}')
            self.share(ramdom_book_id)

    def share(self, cookbook_id):
        data = {
            'cookbook_id': cookbook_id,
        }
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/createCookbookCode'
        response = requests.post(url, headers=self.headers, data=data)
        if not response or response.status_code != 200:
            print("获取分享cookBook失败")
            return
        response_json = response.json()
        if response_json["error_code"] == 0:
            code_url = response_json['data']['code_url'].replace("https://kraftheinzcrm-uat.kraftheinz.net.cn/?", "")
            print(f"获取分享文章链接成功: {code_url}")
            share_records.append(code_url)

    def help(self, tokens):
        try:
            if len(tokens) == 1:
                print("账号不足2个,自己不能给自己助力")
                return
            for i in range(len(tokens)):
                url = {
                    'url': 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/recordScoreShare',
                    'headers': {
                        'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
                        'token': tokens[i]
                    },
                    'body': share_records[(i + 1) % len(tokens)]
                }
                response = requests.post(url['url'], headers=url['headers'], data=url['body'])
                result = response.json()
                if response and response.status_code == 200 and result.get('error_code') == 0:
                    if i + 1 == len(tokens):
                        print(f"账号最后一位助力首账号成功: {result['msg']}")
                    else:
                        print(f"账号{i + 2}被助力成功: {result['msg']}")
                else:
                    print("内部互助失败")
                time.sleep(1)
        except Exception as e:
            print(f"Exception in recordshare function: {str(e)}")

    def exchange_reward(self):
        data = {
            'value': '全网10元话费',
            'phone': '17854279565',
            'type': '话费',
            'memberId': '302061',
        }

        response = requests.post(
            'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/exchangeIntegralNew',
            headers=self.headers,
            data=data,
        )
        print(response.text)

    def score_info_notify(self):
        url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/getUserInfo'
        response_json = requests.get(url, headers=self.headers).json()
        if response_json['error_code'] == 0:
            score = response_json['data']['memberInfo']['score']
            msg = f'💰当前总积分: {score}'
            print(msg)
            if score >= 1000:
                send("卡夫亨积分达标通知", msg)

    def main(self):
        self.user_info()
        self.sign()
        time.sleep(random.randint(5, 10))
        self.share_cookbook_task()


if __name__ == '__main__':
    env_name = 'KFH_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    try:
        # 解析 JSON 字符串
        json_data = json.loads(tokenStr)
        print(f"共获取到{len(json_data)}个账号")
    except json.JSONDecodeError:
        print('⛔️ JSON 解析失败，请检查变量格式是否正确')
        exit(0)

    tokens = []

    for i, token_data in enumerate(json_data, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        token = token_data.get('token')
        user_id = token_data.get('id')
        tokens.append(token)
        # 开始任务
        jsb = JSB(token)
        jsb.main()
        print("\n随机等待10-15s进行下一个账号")
        time.sleep(random.randint(10, 15))
        if i == len(tokens):
            jsb.help(tokens)
