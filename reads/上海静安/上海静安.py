"""
上海静安

抓任意包请求头 token
变量名: SHJA_TOKEN

cron: 13 8 * * *
const $ = new Env("上海静安");
"""
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import make_request, qianwen_messages, save_result_to_file
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SHJA():
    name = "上海静安"

    def __init__(self, account_info):
        self.token = account_info.split('#')[0]
        self.isComment = account_info.split('#')[1]
        self.verify = False
        self.headers = {
            'Host': 'jaapi.shmedia.tech',
            'Accept': '*/*',
            'version': '3.2.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'token': self.token,
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'JingAn/3.2.2 (iPhone; iOS 16.6; Scale/3.00)',
            'Connection': 'keep-alive'
        }

    def userinfo(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/personal/get'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response['code'] == 0:
            save_result_to_file("success", self.name)
            print("----------------------------")
            print(f'🧑‍✈️账号：{response["data"]["nickname"]}')
            print(f'🧑‍✈️积分：{response["data"]["fullScore"]}')
            print("----------------------------")
        else:
            save_result_to_file("error", self.name)
            print(f'❌获取用户信息失败：{response}')

    def login_score(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/points/login/add'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        # print(response)
        if response and response['code'] == 0:
            print("登录任务执行成功")

    def sign(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/personal/score/sign'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            print(f'✅{response["data"]["title"]}')
        else:
            print(f'❌签到任务失败：{response}')

    def total_score(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/personal/score/total'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅当前总积分：{response["data"]["score"]}')
        else:
            print(f'❌总积分获取失败：{response}')

    def today_score(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            print(f'✅今日新增积分：{response["data"]["todayIncreasePoint"]}')
            # return response["data"]["jobs"]
        else:
            print(f'❌今日积分获取失败：{response}')

    def task_list(self):
        json_data = {'id': 'string'}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            today_scores = response["data"]["todayPoint"]
            jobs = response["data"]["jobs"]
            print("-----------------------")
            print(f'🐹🐹🐹任务列表🐹🐹🐹')
            print("-----------------------")
            for i in jobs:
                if "完善个人资料" in i["title"] or "填写邀请码" in i["title"]:
                    continue
                now_pro = f'{i["progress"]}/{i["totalProgress"]}'
                print(f'👻{i["title"]}: {"已完成" if i["status"] == "1" else now_pro}')
            print("-----------------------")
            print(f'👀今日新增积分: {today_scores}')

        return response

    def article_list(self):
        json_data = {
            'orderBy': 'release_desc',
            'channel': {
                'id': 'bf43bbcfd13e4b7ca7692e8a4629f461',
            },
            'pageSize': 50,
            'pageNo': 1,
        }
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/news/content/list'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            return response["data"]["records"]
        else:
            print(f'❌获取文章列表失败：{response}')
            return None

    def article_read_task(self, id):
        status_codes = []
        # 阅读
        json_data = {
            'id': id,
        }
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/news/content/get'
        response_get = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response_get and response_get['code'] == 0:
            status_codes.append(response_get.get('code', None))

        # 扣减
        json_data = {
            'id': id,
            'countType': 'contentRead',
        }
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/common/count/usage/inc'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            status_codes.append(response.get('code', None))

        # 积分
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/points/read/add'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            status_codes.append(response.get('code', None))

        if all(code == 0 for code in status_codes):
            print(f'✅文章{id} 阅读成功')
        else:
            print(f'文章{id}阅读失败：{response_get}')

    def article_favor_task(self, id):
        status_codes = []

        json_data = {
            'id': id,
        }
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/news/content/get'
        response_content = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response_content and response_content['code'] == 0:
            if response_content['data']['count']["favorite"] is True:
                print(f'已经收藏过了，不再重复收藏')
            elif response_content['data']['count']["favorite"]:
                print(f'已经收藏过了，不再重复收藏')
            else:
                # 收藏
                json_data = {
                    'id': id,
                }
                url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/news/content/favor'
                response_favor = make_request(url, json_data=json_data, method='post', headers=self.headers)
                if response_favor and response_favor['code'] == 0:
                    status_codes.append(response_favor.get('code', None))

                # 积分
                json_data = {}
                url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/points/favor/add'
                response = make_request(url, json_data=json_data, method='post', headers=self.headers)
                if response and response['code'] == 0:
                    status_codes.append(response.get('code', None))

                if all(code == 0 for code in status_codes):
                    print(f'✅文章{id} 收藏成功')
                else:
                    print(f'❌文章{id} 收藏失败：{response_favor}')
        else:
            print(f'❌文章{id} 获取失败：{response_content}')

    def article_share_task(self, id):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/points/share/add'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            print(f'✅文章{id} 分享成功')
        else:
            print(f'❌文章{id} 分享失败：{response}')

    def video_view_task(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/points/video/add'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['code'] == 0:
            print(f'✅一条视频已经观看完成')
        else:
            print(f'❌视频观看失败：{response}')

    # 直播
    def live_streaming(self):
        json_data = {}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/points/live/add'
        make_request(url, json_data=json_data, method='post', headers=self.headers)

    def article_content(self, id):
        json_data = {'id': id}
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/news/content/get'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            return response
        else:
            return None

    def get_gpt_comment(self, id):
        basic_news_question = '我需要你针对下面的文章，从一个民众的角度进行评论，我希望你的输出只有评论内容，没有别的无关紧要的词语，回复格式是：芝麻开门#你的评论#， 评论要日常化，字数在10-25字之间，下面是我需要你发表评论的文章内容：'
        article_concent = ''
        response = self.article_content(id)
        comment = ''
        commentCount = 0
        if response and response['code'] == 0:
            commentCount = response["data"]["count"]["commentCount"]
            if commentCount <= 0:
                content = response["data"]["txt"]
                soup = BeautifulSoup(content, 'html.parser')
                content_text = soup.get_text()
                message = qianwen_messages(basic_news_question, content_text)
                comment = message

        return comment

    def article_comment_add(self, id, content):
        json_data = {
            'displayResources': [],
            'content': content,
            'targetType': 'content',
            'targetId': id,
        }
        url = 'https://jaapi.shmedia.tech/media-basic-port/api/app/common/comment/add'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        if response and response["code"] == 0:
            print(f'✅文章评论成功')
        else:
            print(f'❌文章评论失败，{response}')

    def article_comment_task(self, id):
        comment = self.get_gpt_comment(id)
        if comment == '':
            print(f'😢未知错误或者文章可能评论过，算了吧，下一个')
        else:
            parts = comment.split('#')
            if len(parts) > 1:
                comment = parts[1].strip()
            print(f'🐌预评论内容：【{comment}】, 你没意见我就在20s后评论了哈......')
            time.sleep(random.randint(20, 25))
            self.article_comment_add(id, comment)

    def gift_list(self):
        # todo
        print('--------------------')
        print('🐹🐹🐹可兑换商品列表🐹🐹🐹')
        print('--------------------')
        print('😂积分太少啦，暂无商品可兑换')

    def main(self):
        counter = 0
        self.userinfo()
        self.sign()
        for i in range(5):
            self.video_view_task()
            time.sleep(random.randint(20, 30))
        article_list = self.article_list()
        for i in range(10):
            article_id = random.choice(article_list)["id"]
            print('--------------------------------------------------------------------')
            print(f'🐹随机抓取到文章{article_id}，开始任务......')
            self.article_read_task(article_id)
            time.sleep(random.randint(20, 30))
            self.article_share_task(article_id)
            time.sleep(random.randint(10, 18))
            if counter <= 5:
                if self.isComment == '1':
                    self.article_comment_task(article_id)
                    time.sleep(random.randint(20, 40))
                else:
                    print("⛔️未开启自动评论, 如要开启，请更改环境变量配置")
                    time.sleep(random.randint(10, 25))
                self.article_favor_task(article_id)
                time.sleep(random.randint(10, 20))
            counter += 1
        self.task_list()
        self.total_score()
        self.today_score()
        self.gift_list()


if __name__ == '__main__':
    env_name = 'SHJA_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"上海静安共获取到{len(tokens)}个账号")
    for i, account_info in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        SHJA(account_info).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
