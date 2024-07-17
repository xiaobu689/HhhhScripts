"""
中国人保

路径：我的-签到点进去，
抓https://mp.picclife.cn/dop/scoremall/score/internal/scoreAccount/queryMyScoreAccount请求头 x-app-auth-token
变量名: ZGRB_TOKEN
token有效期太短，应该30分钟吧，每天运行一次

cron: 35 23 * * *
const $ = new Env("中国人保");
"""
import os
import random
import time
from datetime import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class ZGRB():
    name = "中国人保"

    def __init__(self, token):
        UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PBrowser/3.16.0 PiccApp/6.22.6 &&webViewInfo=3.16.0&&appInfo=piccApp&&appVersion=6.22.6'
        openId, deviceId = token.split('#')
        self.openId = openId
        self.deviceId = deviceId
        self.access_token = ''
        self.mToken = ''
        self.pre_score = 0
        self.headers = {
            'Host': 'mp.picclife.cn',
            'x-app-auth-type': 'APP',
            'User-Agent': UA,
            'x-app-auth-token': token,
            'x-app-score-channel': 'picc-app001',
            'x-app-score-platform': 'picc-app'
        }


    # TODO CK续期暂未实现，后面再研究
    def third_party_login(self):
        headers = {
            'Host': 'zgrb.epicc.com.cn',
            'X-Tingyun': 'c=A|yeBp8vPsvk4',
            'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'Content-Type': 'application/json',
            # 'Content-Length': '400',
            'User-Agent': 'aasi/6.22.8 (iPhone; iOS 16.6; Scale/3.00)',
            'Connection': 'keep-alive',
            # 'Cookie': 'epicc_ntid=AAAAAWaThtcEvzpOXkZPAg==',
            'X-Tingyun-Id': '4Nl_NnGbjwY;c=2;r=33627;u=05acc997ce32fa199fd98065de0a4a56::BD4E4C616020FB61',
        }
        json_data = {
            'head': {
                'appInfo': {
                    'appVersion': '6.22.8',
                    'appBuild': '286',
                },
                'tags': {
                    'tags': [],
                    'tagsLogin': [],
                },
                'adCode': '310000',
                'deviceInfo': {
                    'deviceId': '2AF394DC-FA35-436C-B891-44A75246CFB2',
                    'osType': 'iOS',
                    'deviceModel': 'iPhone14,7',
                    'osVersion': '16.600',
                    'romType': '',
                    'romVersion': '',
                },
                'userId': '',
            },
            'body': {
                'signInType': '0',
                'thirdPartyId': 'oF3RGt88hPTwIFP0ZQW6DN5jTpK8',
            },
            'uuid': 'e7b68303-2a0b-47fc-a947-f913a4903678',
        }

        response = requests.post(
            'https://zgrb.epicc.com.cn/G-BASE/a/user/login/thirdPartyLogin/v1',
            headers=headers,
            json=json_data,
        )
        print(response.text)
        ck = response.headers.get('Authorization')
        print(ck)
        return ck

    def gen_token(self, ck):
        url = "zgrb.epicc.com.cn"
        url2 = "mp.picclife.cn"
        url3 = "piccapp-2024khj.maxrocky.com"
        url_ = f"https://{url}/G-OPEN/oauth2/authorize/v1?client_id=EC8XhCVQNN5dha8huaRZEC1v&scope=auth_user&response_type=code&redirect_uri=https%3A%2F%2F{url2}%2Fdop%2Fscoremall%2Fuser%2FappLoginCallback%3FafterLoginRedirectUrl%3Dhttps%2525253A%2525252F%2525252F{url2}%2525252Fdop%2525252Fscoremall%2525252Fmall%25252523%2525252FdailyAttendance%2525253Fapply%2525253Dapp"
        print("url_=", url_)
        lj = requests.get(url_, headers={"Cookie": f"w_a_t={ck}"}, verify=False, allow_redirects=False)
        print(lj.text)
        token = requests.get(lj.headers.get('Location'), verify=False).headers.get('app-token')
        print("token=", token)
        return token

    def sign(self):
        json_data = {}
        url = 'https://mp.picclife.cn/dop/scoremall/coupon/ut/signIn/get'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print('签到异常')
            return
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            totalSignInDays = response_json['result']['totalSignInDays']
            print(f'签到成功 | 总签到天数：{totalSignInDays}天')
        else:
            print(f'签到失败 | {response_json["resultMsg"]}')

    def do_task(self):
        json_data = {
            'type': 1,
            'ver': 'AZzqU5arEd+1YXgLSgr0wyGpIm9skwPB6eiUvGy/Zr3hIdPaVurjPj7RIWkj/pajI55+k4Tl4DD3FXynTceGXJl38rlK4ZPkDSUXaHlQjcwuOlJAdJ0hubpv0NYfkbDa93UQj1uTftP2GMaRydkmca/TuZXKMJVoVcPzZj8uUnCS/EN2BpTSWJ/YvZ9zgSOz6C1GWZO6MwF8kcEE2aR50RlH9230JqqIUIWrAFO9VQ1UBUmBSZOzDyDxUaBlHVAkUPeOM0YaT7wd/kXk/JmCgduy2k3fy974XyNObW+xDBssgpZa72k6DOHot/gCoZZnAfF4OgFEesMRz80TcfsgPQ==',
            'localizedModel': '',
            'platform': '',
        }
        url = 'https://mp.picclife.cn/dop/scoremall/coupon/ut/task/list'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print('获取任务列表信息异常')
            return
        response_json = response.json()
        if response_json['resultCode'] != "0000":
            print(f'获取任务列表失败 | {response_json["resultMsg"]}')
            return
        list = response_json['result']['taskList']
        for task in list:
            name = task['name']
            doneTime = task['doneTime']
            if doneTime == 0:
                self.complate_task(task['id'], name)
                time.sleep(random.randint(10, 15))

    def get_points(self):
        json_data = {}
        url = 'https://mp.picclife.cn/dop/scoremall/score/internal/scoreAccount/queryMyScoreAccount'
        response = requests.post(url, headers=self.headers, json=json_data)
        print(response.text)
        if not response or response.status_code != 200:
            print('获取积分信息异常')
            return False
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            totalScore = response_json["result"]["totalScore"]
            availableScore = response_json["result"]["availableScore"]
            self.pre_score = totalScore
            print(f'💰总积分: {totalScore} | 可用积分：{availableScore}')
            return True
        else:
            print(f'获取积分余额失败 | {response_json["resultMsg"]}')
            return False

    def complate_task(self, taskId, name):
        json_data = {
            'businessId': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'taskId': taskId,
        }
        url = 'https://mp.picclife.cn/dop/scoremall/coupon/ut/task/complete'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print('任务完成异常')
            return
        response_json = response.json()
        if response_json['resultCode'] == "0000":
            print(f'🐱{name} | ✅任务完成')
        else:
            print(f'🐱{name} | ❌任务失败 | {response_json["resultMsg"]}')

    def get_diff_score(self):
        json_data = {}
        url = 'https://mp.picclife.cn/dop/scoremall/score/internal/scoreAccount/queryMyScoreAccount'
        response_json = requests.post(url, headers=self.headers, json=json_data).json()
        if response_json['resultCode'] == "0000":
            totalScore = response_json["result"]["totalScore"]
            diff_score = totalScore - self.pre_score
            print(f'💰总积分: {totalScore} | 今日新增积分: {diff_score}')

    def main(self):
        self.gen_token(1)
        exit(0)
        print(f"\n======== ▷ 日常任务 ◁ ========")
        if self.get_points():
            self.sign()
            time.sleep(random.randint(10, 15))
            self.do_task()


if __name__ == '__main__':
    env_name = 'ZGRB_TOKEN'
    token = os.getenv(env_name)
    token = 'oF3RGt88hPTwIFP0ZQW6DN5jTpK8#2AF394DC-FA35-436C-B891-44A75246CFB2'
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    ZGRB(token).main()
