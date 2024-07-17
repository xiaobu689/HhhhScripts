"""
上海嘉定

抓任意包请求头 token
变量名: SHJD_TOKEN

cron: 20 6 * * *
const $ = new Env("上海嘉定");
"""
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import qianwen_messages, save_result_to_file
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SHJD():
    name = "上海嘉定"

    def __init__(self, account_info):
        self.token = account_info.split('#')[0]
        self.isComment = account_info.split('#')[1]
        self.verify = False
        self.totalScore = 0
        self.giftHeaders = {
            'Host': 'mall-api.shmedia.tech',
            'Authorization': self.token,
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://mall-mobile.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/JiaDing; Version/3.1.8',
            'Referer': 'https://mall-mobile.shmedia.tech/',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty'
        }
        self.headers = {
            'Host': 'jdweb.shmedia.tech',
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'token': self.token,
            'Origin': 'https://jdweb.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/JiaDing; Version/3.1.8',
            'Referer': 'https://jdweb.shmedia.tech/app_jd/jd_zwxx/20240506/74f4f9713a684badb145f3ddf2ae47c8.html',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty'
        }

    def login_add(self):
        json_data = {}
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/points/login/add'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print(f'✅账号登录任务完成')
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)

    def userinfo(self):
        json_data = {}
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/personal/get'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                save_result_to_file("success", self.name)
                print("----------------------------")
                print(f'🧑✈️‍账号：{response_json["data"]["mobile"]}')
                print(f'🧑‍✈️积分：{response_json["data"]["score"]}')
                print("----------------------------")
            else:
                save_result_to_file("error", self.name)
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            save_result_to_file("error", self.name)
            print("JSON decode error:", e)

    def sign(self):
        json_data = {}
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/personal/score/sign'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print(f'✅{response_json["data"]["title"]}')
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)

    def today_score(self):
        json_data = {
            'id': 'string',
        }
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print("-----------------------")
                print(f'✅总积分：{response_json["data"]["totalScore"]}')
                print(f'✅今日新增积分：{response_json["data"]["todayPoint"]}')
                self.totalScore = response_json["data"]["totalScore"]
                return response_json
            else:
                print("HTTP request failed with status code:", response.status_code)
                return None
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None

    def task_list(self):
        json_data = {
            'id': 'string',
        }
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/personal/score/info'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print("-----------------------")
                print(f'🐹🐹🐹任务列表🐹🐹🐹')
                print("-----------------------")
                for i in response_json['data']['jobs']:
                    if "完善个人资料" in i["title"] or "填写邀请码" in i["title"]:
                        continue
                    print(f'👻{i["title"]}: {"已完成" if i["status"] == "1" else "未完成"}')
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)

    def article_list(self):
        json_data = {
            'orderBy': 'release_desc',
            'channel': {
                'id': '9b84ad9dd9664184958bfe83c97d4073',
            },
            'pageSize': '50',
            'pageNo': 1,
        }
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/news/content/list'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                return response_json["data"]["records"]
            else:
                print("HTTP request failed with status code:", response.status_code)
                return None
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None

    def article_read_points_add(self):
        json_data = {}
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/points/read/add'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)

    def article_content(self, id):
        json_data = {
            'id': id,
        }
        url = 'https://jdweb.shmedia.tech/media-basic-port/api/app/news/content/get'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                return response_json
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Response content:", response.text)

    def article_read(self, id):
        response = self.article_content(id)
        if response and response['code'] == 0:
            self.article_read_points_add()
            print(f'✅文章阅读成功')
        else:
            print(f'❌阅读失败，{response}')

    def article_favor(self, id):
        response_content = self.article_content(id)
        if response_content and response_content['code'] == 0:
            if response_content['data']['count']["favorite"] is False:
                json_data = {
                    'id': id,
                }
                url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/news/content/favor'
                try:
                    response = requests.post(url, headers=self.headers, json=json_data)
                    if response.status_code == 200:
                        response_json = response.json()
                        print(f'✅文章收藏成功')
                    else:
                        print("HTTP request failed with status code:", response.status_code)
                except requests.exceptions.JSONDecodeError as e:
                    print("JSON decode error:", e)
                    print("Response content:", response.text)
            elif response_content['data']['count']["favorite"]:
                print(f'已经收藏过了，不再重复收藏')
            else:
                print(f'❌收藏失败，{response_content}')
        else:
            print(f'❌获取文章失败，{response_content}')


    def article_share(self, id):
        json_data = {}
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/points/share/add'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print(f'✅文章分享成功')
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Response content:", response.text)

    def video_view_add(self):
        json_data = {}
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/points/video/add'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print(f'✅看片儿完成+1')
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Response content:", response.text)

    def get_gpt_comment(self, id):
        basic_news_question = '我需要你针对下面的文章，从一个民众的角度进行评论，我希望你的输出只有评论内容，没有别的无关紧要的词语，回复格式是：芝麻开门#你的评论#， 评论要日常化，字数一定要限制在7-15字之间，下面是我需要你发表评论的文章内容：'
        article_concent = ''
        response = self.article_content(id)
        comment = ''
        commentCount = 0
        if response is not None and response['code'] == 0:
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
        url = 'https://jdapi.shmedia.tech/media-basic-port/api/app/common/comment/add'
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code == 200:
                response_json = response.json()
                print(f'✅文章评论成功')
            else:
                print("HTTP request failed with status code:", response.status_code)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Response content:", response.text)

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

    def main(self):
        self.userinfo()
        self.sign()
        for i in range(10):
            self.video_view_add()
            time.sleep(random.randint(20, 30))
        article_list = self.article_list()
        for i in range(10):
            article_id = random.choice(article_list)["id"]
            print('--------------------------------------------------------------------')
            print(f'🐹随机抓取到一篇文章{article_id}，开始做任务......')
            self.article_read(article_id)
            time.sleep(random.randint(20, 35))
            self.article_comment_task(article_id)
            time.sleep(random.randint(10, 20))
            self.article_share(article_id)
            time.sleep(random.randint(10, 18))
            if self.isComment == '1':
                print("⛔️评论功能已关闭，如需开启，请更改环境变量配置")
                # self.article_comment_task(article_id)
                # time.sleep(random.randint(20, 40))
            else:
                print("⛔️未开启自动评论, 如要开启，请更改环境变量配置")
                time.sleep(random.randint(10, 25))
            # self.article_favor(article_id)
            # time.sleep(random.randint(10, 20))
        self.task_list()
        self.today_score()


if __name__ == '__main__':
    env_name = 'SHJD_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"上海嘉定共获取到{len(tokens)}个账号")
    for i, account_info in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        SHJD(account_info).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
