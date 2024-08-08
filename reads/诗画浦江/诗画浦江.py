"""
诗画浦江

变量名: SHPJ
cron: 52 8 * * *
const $ = new Env("诗画浦江");
"""
import os
import random
import re
import time
import hashlib
import uuid
from common import save_result_to_file
import requests
from urllib.parse import quote
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning


class SHPJ():
    name = "诗画浦江"

    def __init__(self, token):
        self.mobile = token.split('#')[0]
        self.pwd = token.split('#')[1]
        self.code = ''
        self.account_id = ''
        self.session_id = ''
        self.device_id = ''
        self.pre_integral = 0
        self.is_comment = 0  # 0关闭 1开启

    def login(self):
        headers = {
            'Host': 'vapp.tmuyun.com',
            'X-TIMESTAMP': '1721289326713',
            'X-SESSION-ID': '6697e311eb852e76c6e3e292',
            'Accept': '*/*',
            'X-SIGNATURE': '9d80f2c1acd5e6b4c5a6baf6578735b7018d297dbb8f6e6383d51e3eebd315b3',
            'X-TENANT-ID': '14',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'X-REQUEST-ID': '25BC176A-BCFE-41F5-A177-598603AD21B8',
            'User-Agent': '1.3.1;655520DC-629B-4D4C-89D3-AFF5965BAB73;iPhone8,1;IOS;13.4.1;Appstore;6.12.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'code': self.code,
        }

        response = requests.post('https://vapp.tmuyun.com/api/zbtxz/login', headers=headers, data=data)
        response_json = response.json()
        if response_json["code"] == 0:
            print("登陆成功")
            session_id = response_json["data"]["session"]["id"]
            account_id = response_json["data"]["session"]["account_id"]
            device_id = response_json["data"]["session"]["device_id"]
            self.account_id = account_id
            self.device_id = device_id
            self.session_id = session_id
        else:
            print(f"登陆失败 | {response_json['message']}")
            exit(0)

    def user_info(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/account_detail'
        headers = self.gen_headers(url)
        params = {
            'osTypeCode': '2',
        }
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        if response_json["code"] == 0:
            nick_name = response_json["data"]["rst"]
            phone = response_json["data"]["rst"]["mobile"]
            total_integral = response_json["data"]["rst"]["total_integral"]
            self.pre_integral = total_integral
            print(f"昵称：{nick_name} | 手机号：{phone} | 积分：{total_integral}")

    def score_info(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/account_detail'
        headers = self.gen_headers(url)
        params = {
            'osTypeCode': '2',
        }
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        if response_json["code"] == 0:
            nick_name = response_json["data"]["rst"]
            phone = response_json["data"]["rst"]["mobile"]
            total_integral = response_json["data"]["rst"]["total_integral"]
            diff_scores = total_integral - self.pre_integral
            print(f"昵称：{nick_name} | 手机号：{phone}")
            print(f'总积分：{total_integral}')
            print(f"今日新增积分：{diff_scores}")

    # 任务列表
    def task(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/numberCenter'
        headers = self.gen_headers(url)
        params = {
            'is_new': '1',
            'refer__1540': 'n4+xnDRD07itefxUx0v+bmYBe7uhixxTD',
        }
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        # 随机获取文章
        article_list = self.article_list()
        print(f"文章数量: {len(article_list)}")
        if len(article_list) <= 0:
            print("没有文章")
            return
        if response_json["code"] == 0:
            list = response_json["data"]["rst"]["user_task_list"]
            for item in list:
                id = item["id"]
                completed = item["completed"]  # 0未完成 1已完成
                finish_times = item["finish_times"]  # 完成次数
                frequency = item["frequency"]
                can_do = frequency - finish_times
                name = item["name"]
                if completed == 1:
                    print(f"{id}|{name} |任务已完成")
                    continue
                # 新闻资讯阅读
                if id == 134:
                    for i in range(can_do):
                        print(f'{name}|{i+1}/{can_do}')
                        # 随机获取文章
                        article = random.choice(article_list)
                        article_id = article["id"]
                        channel_id = article["channel_id"]
                        print(f'文章ID: {article_id} | 分类ID: {channel_id}')
                        self.read(channel_id, article_id)
                        time.sleep(random.randint(5, 15))
                # 分享资讯给好友
                elif id == 135:
                    for i in range(can_do):
                        print(f'{name}|{i+1}/{can_do}')
                        # 随机获取文章
                        article_id = random.choice(article_list)["id"]
                        self.share(article_id)
                        time.sleep(random.randint(5, 15))
                # 新闻资讯评论
                elif id == 136:
                    print("评论开关：", self.is_comment)
                    if self.is_comment == "1":
                        for i in range(can_do):
                            print("假装在评论")
                            print(f'{name}|{i + 1}/{can_do}')
                            # 随机获取文章
                            article_id = random.choice(article_list)["id"]
                            self.comment(article_id)
                            time.sleep(random.randint(5, 15))
                    else:
                        print("评论开关已关闭, 如需评论，请打开开关")
                # 新闻资讯点赞
                elif id == 137:
                    print(f"还可以点赞次数:{can_do}")
                    for i in range(can_do):
                        print(f'{name}|{i + 1}/{can_do}')
                        # 随机获取文章
                        article_id = random.choice(article_list)["id"]
                        print(f'文章ID: {article_id}')
                        self.like(article_id)
                        time.sleep(random.randint(5, 15))
                # 使用本地服务
                elif id == 138:
                    for i in range(can_do):
                        print(f'{name}|{i + 1}/{can_do}')
                        self.use_local_service()
                        time.sleep(random.randint(5, 15))

    def article_comment_list(self, article_id):
        url = 'https://vapp.tmuyun.com/api/comment/list'
        headers = self.gen_headers(url)
        params = {
            'channel_article_id': article_id,
            'size': '20',
            'sort_type': '0',
        }
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        if response_json["code"] == 0:
            list = response_json["data"]["comment_list"]
            return list
        else:
            return []

    def read(self, channel_id, article_id):
        url = 'https://vapp.tmuyun.com/api/article/detail'
        headers = self.gen_headers(url)
        params = {
            'hz_channnel_id': channel_id,
            'id': article_id,
            'tenantId': '14',
            'url_Path': '/webDetails/news'
        }
        response_json = requests.get(url, params=params, headers=headers).json()
        if response_json["code"] == 0:
            print(f"阅读成功")
        else:
            print(f"阅读失败 | {response_json['message']}")

    def like(self, article_id):
        url = 'https://vapp.tmuyun.com/api/favorite/like'
        headers = self.gen_headers(url)

        data = {
            'action': '1',
            'id': article_id,
        }
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json["code"] == 0:
            print("点赞成功")
        else:
            print(f"点赞失败 | {response_json['message']}")

    def comment(self, article_id):
        url = 'https://vapp.tmuyun.com/api/comment/create/v2'
        headers = self.gen_headers(url)
        headers['Content-Type'] = 'application/json'
        json_data = {
            'channel_article_id': article_id,
            'links': [],
            'content': '不错，赞',
        }

        response = requests.post(url, headers=headers, json=json_data)
        response_json = response.json()
        if response_json["code"] == 0:
            print("评论成功")
        else:
            print(f"评论失败 | {response_json['message']}")

    def share(self, article_id):
        url = 'https://vapp.tmuyun.com/api/user_mumber/doTask'
        headers = self.gen_headers(url)
        data = {
            'member_type': '3',
            'target_id': article_id,
        }
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json["code"] == 0:
            print("分享成功")
        else:
            print(f"分享失败 | {response_json['message']}")

    def use_local_service(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/doTask'
        headers = self.gen_headers(url)
        data = {
            'member_type': '6',
        }
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json["code"] == 0:
            print("使用本地服务成功")
        else:
            print(f"使用本地服务失败 | {response_json['message']}")

    def sign(self):
        url = 'https://vapp.tmuyun.com/api/user_mumber/sign'
        headers = self.gen_headers(url)

        params = {
            'refer__1540': 'n4Uxgi0Qo7qGwqiqGNDQTiQeGQB=E4AI=qIAmQx',
        }

        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        if response_json["code"] == 0:
            print("签到成功")
        else:
            print(f"签到失败 | {response_json['message']}")

    def article_list(self):
        url = 'https://vapp.tmuyun.com/api/article/channel_list'
        headers = self.gen_headers(url)
        channel_ids = [
            "5cc02969b1985017d6fef804",
            "5cc2ccbe1b011b18ee37591d",
            "5d52be161b011b137b853d18",
            "5cc2cc981b011b18ee37591c",
            "5d075f1e1b011b68176a8a00",
            "5f103ebaad61a40f3c8cce88",
            "5d64c2ea1b011b2a0fbba127",
            "622b01cdfe3fc10794f6c747"
        ]
        channel_id = random.choice(channel_ids)
        params = {
            'channel_id': channel_id,
            'is_new': '1',
            'size': '50',
        }

        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        if response_json["code"] == 0:
            list = response_json["data"]["article_list"]
            return list
        else:
            return []

    def sha256(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def generate_custom_uuid(self):
        # 生成一个UUID
        generated_uuid = uuid.uuid4()

        # 将UUID转换为指定格式字符串，例如：04D273CE-FAE2-4CC8-B020-E172B063ED8E
        formatted_uuid = str(generated_uuid).upper()

        return formatted_uuid

    def gen_headers(self, url):
        url = url.replace("https://vapp.tmuyun.com", "")
        path = url.split('?')[0]
        timestamp = int(time.time() * 1000)

        key = "FR*r!isE5W"
        uuid = self.generate_custom_uuid()
        str_to_hash = f'{path}&&{self.session_id}&&{uuid}&&{timestamp}&&{key}&&14'

        sign = self.sha256(str_to_hash)
        headers = {
            'Host': 'vapp.tmuyun.com',
            'X-TIMESTAMP': f'{timestamp}',
            'X-SESSION-ID': self.session_id,
            'Accept': '*/*',
            'X-SIGNATURE': sign,
            'X-TENANT-ID': '14',
            'X-ACCOUNT-ID': self.account_id,
            'Accept-Language': 'zh-Hans-CN;q=1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-REQUEST-ID': uuid,
            'User-Agent': '2.0.3;DF906D4C-3F54-424A-9162-99AD9B10AED5;iPhone8,1;IOS;13.4.1;Appstore;6.10.0'
        }
        return headers

    def rsa_encrypt(self, data):
        url = "https://www.bejson.com/Bejson/Api/Rsa/pubEncrypt"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "www.bejson.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        }
        body = {
            "publicKey": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD6XO7e9YeAOs+cFqwa7ETJ+WXizPqQeXv68i5vqw9pFREsrqiBTRcg7wB0RIp3rJkDpaeVJLsZqYm5TW7FWx/iOiXFc+zCPvaKZric2dXCw27EvlH5rq+zwIPDAJHGAfnn1nmQH7wR3PCatEIb8pz5GFlTHMlluw4ZYmnOwg+thwIDAQAB\n-----END PUBLIC KEY-----",
            "encStr": data,
            "etype": "rsa2"
        }
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            result = response.json()
            if result["code"] == 200:
                return result["data"]
            else:
                print(result["msg"])
        else:
            print(f"API请求失败，请检查网络重试: {response.status_code}")

    def credential_auth(self):
        rsa_pwd = self.rsa_encrypt(self.pwd)
        url = "https://passport.tmuyun.com/web/oauth/credential_auth"
        body = f"client_id=12&password={quote(rsa_pwd)}&phone_number={self.mobile}"
        headers = {
            "Host": "passport.tmuyun.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br"
        }
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            response_json = response.json()
            if response_json["code"] == 0:
                code = response_json['data']["authorization_code"]["code"]
                self.code = code
            else:
                print(response_json["message"])
        else:
            print(f"API请求失败，请检查网络重试: {response.status_code}")

    def main(self):
        self.credential_auth()
        time.sleep(3)
        self.login()
        time.sleep(random.randint(5, 10))

        self.user_info()
        time.sleep(random.randint(5, 10))

        self.sign()
        time.sleep(random.randint(5, 10))

        self.task()

        self.score_info()


if __name__ == '__main__':
    env_name = 'SHPJ'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"诗画浦江共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        SHPJ(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
