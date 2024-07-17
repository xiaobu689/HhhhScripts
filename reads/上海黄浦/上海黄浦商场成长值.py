"""
上海黄浦商场成长值

变量名: SHHP_MALL_TOKEN
cron: 33 6 * * *
const $ = new Env("上海黄浦商场成长值");
-------------------------------------
20240708 增加成长值达标解锁兑换E卡通知
20240701 增加评论剧目功能
-------------------------------------
"""
import json
import os
import random
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import save_result_to_file
from sendNotify import send
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SHHP_MALL():
    name = "上海黄浦商场成长值"

    def __init__(self, token):
        self.token = token
        self.verify = False
        self.play_ids = []
        self.pre_growth = 0
        self.play_comment_ids = []
        self.headers = {
            'Host': 'hpweb.shmedia.tech',
            'Authorization': token,
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://hpweb.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/HuangPu; Version/2.1.5',
            'Referer': 'https://hpweb.shmedia.tech/show-life-front/?v=2.4',
            'Content-Length': '0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

    def user_mall_info(self):
        url = 'https://hpweb.shmedia.tech/show-life-api/front/member/info'
        response = requests.post(url, headers=self.headers)
        if not response or response.status_code != 200:
            print(f'❌获取用户信息失败，{response.text}')
            save_result_to_file("error", self.name)
            return False
        response_json = response.json()
        if response_json and response_json["code"] == 0:
            nick_name = response_json["data"]["nickname"]
            mobile = response_json["data"]["mobile"]
            growth = response_json["data"]["exp"]
            self.pre_growth = growth
            print(f'✅{nick_name} | {mobile} |{growth}活跃值')
            save_result_to_file("success", self.name)
            return True
        else:
            print(f'❌获取用户信息失败，{response.text}')
            save_result_to_file("error", self.name)
            return False

    def play_mall_task(self):
        url = 'https://hpweb.shmedia.tech/show-life-api/front/task/list'
        response = requests.post(url, headers=self.headers)
        if not response or response.status_code != 200:
            print(f'❌获取任务列表失败，{response.text}')
            return
        response_json = response.json()
        if response_json and response_json["code"] == 0:
            for task in response_json["data"]:
                if task["name"] == "每日访问":
                    print("✅每日访问任务完成")
                    time.sleep(random.randint(5, 10))
                elif task["name"] == "搜索":
                    self.play_search()
                    time.sleep(random.randint(15, 30))
                elif task["name"] == "浏览剧目":
                    self.search_play_list()
                    for i in range(task["dailyLimit"]):
                        self.play_view()
                        time.sleep(random.randint(5, 10))
                elif task["name"] == "评论剧目":
                    self.play_hot_list()
                    self.play_recommend_list()
                    self.play_coming_list()
                    for i in range(task["dailyLimit"]):
                        self.play_comment()
                        time.sleep(random.randint(10, 15))
                elif task["name"] == "点赞评论":
                    for i in range(task["dailyLimit"]):
                        self.great_comment_list()
                        self.comment_like()
                        time.sleep(random.randint(10, 15))
                elif task["name"] == "分享剧目":
                    for i in range(task["dailyLimit"]):
                        self.play_share_complate()
                        time.sleep(random.randint(10, 15))
                        # self.play_share_add()
                        # time.sleep(random.randint(10, 15))
        else:
            print(f'❌获取任务列表失败，{response.text}')

    def play_search(self):
        json_data = {
            'pageNo': 1,
            'pageSize': 10,
            'type': 0,
            'keywords': '恋爱',
        }
        response = requests.post('https://hpweb.shmedia.tech/show-life-api/front/index/serch', headers=self.headers,
                                 json=json_data)

    # 热门剧目
    def search_play_list(self):
        json_data = {
            'pageNo': 1,
            'pageSize': 100,
            'type': 1,
            'typeId': '95ab9c086c335fda0683c4a7598f7c5f',
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/index/serch'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']['records']
            for item in list:
                self.play_ids.append(item['id'])

    def play_view(self):
        id = random.choice(self.play_ids)
        json_data = {
            'id': id,
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/play/info'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅浏览剧目完成')
        else:
            print(f'浏览剧目失败')

    def play_share_complate(self):
        json_data = {
            'token': self.token,
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/task/complete/share'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅分享剧目完成')
        else:
            print(f'分享剧目失败')

    def great_comment_list(self):
        json_data = {
            'pageNo': 1,
            'pageSize': 20,
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/index/comment/great'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']['records']
            for item in list:
                self.play_comment_ids.append(item['id'])
        else:
            print(f'获取好评列表失败')

    def comment_like(self):
        comment_id = random.choice(self.play_comment_ids)
        json_data = {
            'id': comment_id,
        }
        response = requests.post(
            'https://hpweb.shmedia.tech/show-life-api/front/comment/like',
            headers=self.headers,
            json=json_data,
        )
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅评论点赞完成')
        else:
            print(f'评论点赞失败')

    # 热门榜
    def play_hot_list(self):
        json_data = {
            'size': 100,
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/index/play/hots'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']
            for item in list:
                self.play_ids.append(item['id'])

    # 推荐榜
    def play_recommend_list(self):
        response = requests.get('https://hpweb.shmedia.tech/show-life-api/front/index/play/recList',
                                headers=self.headers)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']
            for item in list:
                self.play_ids.append(item['id'])

    # 即将上映
    def play_coming_list(self):
        json_data = {
            'pageNo': 1,
            'pageSize': 100,
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/index/play/upcomingShows'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']['records']
            for item in list:
                self.play_ids.append(item['id'])

    # 历史剧目
    def play_past_list(self):
        json_data = {
            'pageNo': 1,
            'pageSize': 100,
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/index/play/past'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            list = response_json['data']['records']
            for item in list:
                self.play_ids.append(item['id'])

    def play_comment(self):
        contents = [
            '感觉挺不错的样子，期待更多优秀的作品',
            '这个不错，期待，希望自己有机会现场感受一下',
            '剧目都好棒，多想有机会全部看完啊',
            '喜欢看剧目的你们一定是一群情感细腻的人',
            '这也想看，那也想看，却忙的啥也看不了，啊啊啊难受',
            '优秀的作品值得反复观看静静品味',
            '我要是有哆啦A梦的神奇口袋多好，嗖一下到现场',
            '这是一场视觉和听觉的盛宴',
            '一边忙于生活，一边觉得应该追求内心的喜欢'
        ]
        play_id = random.choice(self.play_ids)
        content = random.choice(contents)
        json_data = {
            'playId': play_id,
            'watched': 0,
            'rating': 0,
            'content': content,
            'commentMediaList': [],
        }
        url = 'https://hpweb.shmedia.tech/show-life-api/front/comment/postComment'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json and response_json['code'] == 0:
            print(f'✅评论成功 | 剧目ID: {play_id}')
        else:
            print(f'评论失败 | {response_json["message"]}')

    def user_growth_notify(self):
        url = 'https://hpweb.shmedia.tech/show-life-api/front/member/info'
        response_json = requests.post(url, headers=self.headers).json()
        if response_json["code"] == 0:
            nick_name = response_json["data"]["nickname"]
            mobile = response_json["data"]["mobile"]
            growth = response_json["data"]["exp"]
            diff = growth - self.pre_growth
            print('\n-----------------------------------------------------')
            print(f'🐶账号: {nick_name} | 🌱成长值: {growth}成长值 | 🍄今日新增: {diff}')
            # 活跃值达标1200触发通知
            if growth >= 1200:
                message = "上海黄浦成长值达标1200, 解锁20元E卡兑换资格\n"
                message += f'''
                ✨ 规则：
                        900 成长值 - -解锁 - -4000积分兑换腾讯月卡
                        1200成长值 - -解锁 - -4300兑换20元京东E卡
                        8000成长值 - -解锁 - -6600积分兑换30元京东E卡
                ✨ 规则
                '''
                message += f'账号: {mobile}\n'
                send("上海黄浦成长值达标1200", message)

    def main(self):
        if self.user_mall_info():
            self.play_mall_task()
            self.user_growth_notify()


if __name__ == '__main__':
    print(f'''
    ✨ 规则：
            900 成长值 - -解锁 - -4000积分兑换腾讯月卡
            1200成长值 - -解锁 - -4300兑换20元京东E卡
            8000成长值 - -解锁 - -6600积分兑换30元京东E卡
    ✨ 规则
    ''')
    env_name = 'SHHP_MALL_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    try:
        json_data = json.loads(tokenStr)
        print(f"共获取到{len(json_data)}个账号")
    except json.JSONDecodeError:
        print('⛔️ JSON 解析失败，请检查变量格式是否正确')
        exit(0)

    for i, token_data in enumerate(json_data, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        token = token_data.get('token')
        SHHP_MALL(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
