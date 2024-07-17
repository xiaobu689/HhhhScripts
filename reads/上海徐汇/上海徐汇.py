"""
上海徐汇

抓任意包请求头 token
变量名: SHXH_TOKEN

cron: 35 16 * * *
const $ = new Env("上海徐汇");
"""
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

from common import qianwen_messages, make_request, save_result_to_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SHCN():
    name = "上海徐汇"

    def __init__(self, account_info):
        self.token = account_info.split('#')[0]
        self.isComment = account_info.split('#')[1]
        self.verify = False
        self.headers = {
            'Host': 'xhapi.shmedia.tech',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'token': self.token,
            'Content-Type': 'application/json; charset=utf-8',
            'deviceId': 'af223dabdc3b484c8eae7809f6da7ba6',
            'User-Agent': 'StandardApplication/6.2.7 (iPhone; iOS 16.6; Scale/3.00)',
            'Connection': 'keep-alive'
        }

    def login_score(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/points/login/add'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        # print(response)
        if response and response['code'] == 0:
            save_result_to_file("success", self.name)
            print("✅登录任务执行成功")
        else:
            save_result_to_file("error", self.name)

    def sign(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/personal/score/sign'
        response = make_request(url, json_data, 'post', self.headers)
        # print(response)
        if response and response['code'] == 0:
            print(f'✅{response["data"]["title"]}')
        else:
            print(f'❌{response["msg"]}')

    def total_score(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/personal/score/total'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅当前总积分：{response["data"]["score"]}')
        else:
            print(f'❌总积分获取失败：{response}')

    def today_score(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅今日新增积分：{response["data"]["todayIncreasePoint"]}')
            # return response["data"]["jobs"]
        else:
            print(f'❌今日积分获取失败：{response}')

    def task_list(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print("-----------------------")
            print(f'🐹🐹🐹任务列表🐹🐹🐹')
            print("-----------------------")
            for i in response['data']['jobs']:
                if "完善个人资料" in i["title"] or "填写邀请码" in i["title"]:
                    continue
                print(f'👻{i["title"]}: {"已完成" if i["status"] == "1" else "未完成"}')

    def article_list(self):
        json_data = {
            'orderBy': 'release_desc',
            'channel': {
                'id': '6bb94decba2a416d908ad8c108576305',
            },
            'pageSize': 50,
            'pageNo': 1,
        }
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/news/content/list'
        response = make_request(url, json_data, 'post', self.headers)

        return response["data"]["records"]

    def article_read_points_add(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/points/read/add'
        make_request(url, json_data, 'post', self.headers)

    def article_count_usage_desc(self, id):
        json_data = {
            'id': id,
            'countType': 'contentRead',
        }
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/common/count/usage/inc'
        make_request(url, json_data, 'post', self.headers)

    def article_content(self, id):
        json_data = {'id': id}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/news/content/get'
        response = make_request(url, json_data, 'post', self.headers)
        return response

    def article_read(self, id):
        response = self.article_content(id)
        if response and response['code'] == 0:
            self.article_read_points_add()
            self.article_count_usage_desc(id)
            print(f'✅文章阅读成功')
        else:
            print(f'❌阅读失败，{response}')

    def video_view_task(self):
        json_data = {}
        url = 'https://xhapi.shmedia.tech/media-basic-port/api/app/points/video/add'
        response = requests.post(url, headers=self.headers, json=json_data, verify=self.verify).json()
        if response and response['code'] == 0:
            print(f'✅看片儿完成+1')
        else:
            print(f'❌看片儿失败：{response}')

    def gift_list(self):
        # todo
        print('--------------------')
        print('🐹🐹🐹可兑换商品列表🐹🐹🐹')
        print('--------------------')
        print('😂积分太少啦，暂无商品可兑换')

    def main(self):
        self.login_score()
        self.sign()
        for j in range(20):
            self.video_view_task()
            time.sleep(random.randint(20, 30))
        article_list = self.article_list()
        for i in range(22):
            article_id = random.choice(article_list)["id"]
            print('--------------------------------------------------------------------')
            print(f'🐹随机抓取到一篇文章【{i+1}】，开始做任务......')
            self.article_read(article_id)
            time.sleep(random.randint(20, 35))
        self.task_list()
        self.total_score()
        self.today_score()
        self.gift_list()


if __name__ == '__main__':
    env_name = 'SHXH_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"上海徐汇共获取到{len(tokens)}个账号")
    for i, account_info in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        SHCN(account_info).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
