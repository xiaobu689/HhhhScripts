"""
中国人保【抽奖】

超级1+6|每周一、周六、每月尾数逢1，逢6抽奖

变量名: ZGRBCJ
变量： openid，多账号&连接
微信公众号福建人保财险，菜单栏超级1+6抓包openid
cron: 35 6 * * *
const $ = new Env("中国人保【抽奖】");
"""
import os
import random
import re
import time
from datetime import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from sendNotify import send
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

class FJRBCX():
    name = "顺义创城"

    def __init__(self, openid):
        self.openid = openid
        self.encryName = ''
        self.unionid = ''
        self.headers = {
            'Host': 'smsp.epicc.com.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://smsp.epicc.com.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x18003237) NetType/WIFI Language/zh_CN',
            'Referer': 'https://smsp.epicc.com.cn/branches/webpage/webpage/center_xjg/dist/mobile/wechat/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty'
        }

    def login(self):
        json_data = {
            'requestbody': {
                'comCode': '',
                'userName': '',
                'comId': '',
                'agentCode': '0',
                'userId': 'picc-fuj',
                'unionId': '',
                'openId': self.openid,
            },
        }
        url = 'https://smsp.epicc.com.cn/WAS/userLoginApi/autoLogin'
        response = requests.post(url, headers=self.headers, json=json_data, verify=False)
        print(response.text)
        response_json = response.json()
        if response_json["status"] == 0:
            print('登录成功')
            unionid = response_json['data'].get('unionid', '')
            encryName = response_json['data'].get('encryName', '')
            self.unionid = unionid
            self.encryName = encryName

    def lottery(self, activity_id):
        json_data = {
            'header': {
                'openid': self.openid,
                'comCode': '35000000',
                'comId': '35000000',
                'userName': self.encryName,
                'agentCode': '0',
                'token': '',
                'userId': 'picc-fuj',
                'unionId': self.unionid,
            },
            'body': {
                'cmd': 'queryactivitydetail',
                'activityNo': activity_id,
                'memId': '',
                'activityType': '1',
                'transactionNo': '',
                'isDifferWinningRate': '',
            },
        }
        url = 'http://smsp.epicc.com.cn/WAS/recentActivtyApi/themeActivityNew'
        response = requests.post(url, headers=self.headers, json=json_data)
        print(response.text)
        response_json = response.json()
        if response_json["status"] == 0:
            activity_name = response_json['data']["activityName"]
            gift_name = response_json['data']["giftName"]
            if "很遗憾" in gift_name or gift_name is None:
                print('很遗憾，您未中奖！')
            else:
                print(f"{activity_name} {gift_name}")
                msg = f"福建人保财险账号中了{gift_name}"
                send("福建人保中奖", msg)
                print(msg)
        elif response_json["status"] == -1:
            print('很遗憾，您未中奖！')

    def main(self):
        today = datetime.today()
        weekday = today.weekday() + 1
        day = today.day
        # 星期一
        if weekday == 1:
            activity_id = "300009219"
            self.lottery(activity_id)
        # 星期六
        elif weekday == 6:
            activity_id = "300009217"
            self.lottery(activity_id)
        # 每月日期尾数逢1
        if str(day)[-1] == '1':
            activity_id = "300009220"
            self.lottery(activity_id)
        # 每月日期尾数逢6
        elif str(day)[-1] == '6':
            activity_id = "300009218"
            self.lottery(activity_id)
        else:
            print("今日非活动日期")


if __name__ == '__main__':
    env_name = 'FJRBCJ'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"福建人保财险共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        FJRBCX(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(10, 15))

