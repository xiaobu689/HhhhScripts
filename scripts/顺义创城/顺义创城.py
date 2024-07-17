"""
顺义创城

抓任意包请求头 X-Applet-Token
变量名: SYCC_TOKEN

cron: 15 7 * * *
const $ = new Env("顺义创城");
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


class SYCC():
    name = "顺义创城"

    def __init__(self, token):
        self.token = token
        self.issue_ids = []
        self.userId = 0
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

    def sign(self):
        json_data = {}
        url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/ccScoreRecord/signIn'
        response = requests.post(url, headers=self.headers, json=json_data, verify=False)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200 or response_json['code'] == 500:
                print(f'✅签到成功')
            else:
                print(f'❌签到失败， {response_json["message"]}')
        else:
            print(f'❌签到失败')

    def sign_history(self):
        params = {
            'time': '2024-06-11',
        }
        json_data = {}
        response = requests.post(
            'https://admin.shunyi.wenming.city/jeecg-boot/applet/ccScoreRecord/signInHistory',
            params=params,
            headers=self.headers,
            json=json_data,
        )
        if response and response.status_code == 200:
            response_json = response.json()
            # print(response_json["result"])

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
                self.userId = response_json["result"]["id"]
                print(f'✅{name} | {phone} | {score}积分')
            else:
                save_result_to_file("error", self.name)
        else:
            save_result_to_file("error", self.name)

    def issue_list(self):
        params = {
            'activityId': '1422847506301235202',
            'pageNo': '1',
            'pageSize': '100',
            'status': '1422585857430052866',  # 未参与校验
        }
        url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/ccUserActivity/list'
        response = requests.get(url, params=params, headers=self.headers, )
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                list = response_json["result"]
                for item in list:
                    self.issue_ids.append(item["id"])

    def issue_like(self):
        id = random.choice(self.issue_ids)
        params = {
            'id': id,
        }
        json_data = {}
        url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/ccUserActivity/like'
        response = requests.post(url, params=params, headers=self.headers, json=json_data, )
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print('✅点赞成功')
            else:
                print("点赞失败: ", response_json["message"])
        else:
            print("未知错误,", response)

    def like_add_score(self):
        params = {
            'score': '1',
            'type': '15',
            'time': '0',
        }
        url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore'
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print("✅点赞积分增加成功")

    def share_add_score(self):
        params = {
            'score': '1',
            'type': '14',
            'time': '0',
        }
        url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore'
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print("✅分享成功")

    def article_list(self):
        params = {
            'pageNo': '1',
            'pageSize': '20',
            'column': 'isTop,createTime',
            'order': 'desc',
        }
        url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/workNews/list'
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                list = response_json["result"]["records"]

    def view_add_score(self):
        time = random.randint(20000, 30000)
        params = {
            'score': '1',
            'type': '5',
            'time': time,
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print("✅浏览完成")

    def game_xxk_1(self):
        params = {
            'score': '3',
            'type': '12',
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("消消乐第一关：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print("✈️消消乐第一关 | 通关")
        else:
            print("❌消消乐第一关 | 未通关 | 出现异常了")

    def game_xxk_2(self):
        params = {
            'score': '5',
            'type': '16',
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("消消乐第二关：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print("✈️消消乐第二关 | 通关")
        else:
            print("❌消消乐第二关 | 未通关 | 出现异常了")

    def game_xxk_3(self):
        params = {
            'score': '10',
            'type': '17',
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("消消乐第三关：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print("✈️消消乐第三关 | 通关")
        else:
            print("❌消消乐第三关 | 未通关 | 出现异常了")

    def game_xxk_task(self):
        self.game_xxk_1()
        time.sleep(random.randint(30, 60))
        self.game_xxk_2()
        time.sleep(random.randint(40, 70))
        self.game_xxk_3()

    def game_pintu_1(self):
        params = {
            'score': '3',
            'type': '29',
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("拼图第一关：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print("✈️拼图第一关 | 通关")
        else:
            print("❌拼图第一关 | 未通关 | 出现异常了")

    def game_pintu_2(self):
        params = {
            'score': '5',
            'type': '30',
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("拼图第二关：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print("✈️拼图第二关 | 通关")
        else:
            print("❌拼图第二关 | 未通关 | 出现异常了")

    def game_pintu_3(self):
        params = {
            'score': '10',
            'type': '31',
        }
        response = requests.get('https://admin.shunyi.wenming.city/jeecg-boot/applet/user/addScore', params=params,
                                headers=self.headers)
        if not response or response.status_code != 200:
            print("拼图第三关：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print("✈️拼图第三关 | 通关")
        else:
            print("❌拼图第三关 | 未通关 | 出现异常了")

    def game_pintu_task(self):
        self.game_pintu_1()
        time.sleep(random.randint(30, 40))
        self.game_pintu_2()
        time.sleep(random.randint(60, 70))
        self.game_pintu_3()

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
                print(f"🐹抽奖完成 | {award}")
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
        else:
            print("未知错误，赶紧看看吧，", response.text)

    def main(self):
        self.user_info()
        self.issue_list()
        print(f"\n======== ▷ 签到浏览点赞 ◁ ========")
        self.sign()
        time.sleep(random.randint(10, 15))
        self.article_list()
        for i in range(3):
            if i <= 1:
                self.issue_like()
                self.like_add_score()
                time.sleep(random.randint(10, 15))
            self.view_add_score()
            time.sleep(random.randint(5, 10))

        print(f"\n======== ▷ 消消卡游戏 ◁ ========")
        self.game_xxk_task()
        time.sleep(random.randint(10, 15))
        self.share_add_score()
        time.sleep(random.randint(10, 15))

        print(f"\n======== ▷ 拼图游戏 ◁ ========")
        self.game_pintu_task()
        time.sleep(random.randint(5, 15))

        print(f"\n======== ▷ 抽奖 ◁ ========")
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
