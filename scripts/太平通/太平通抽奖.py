"""
太平通抽奖

cron: 0 0 * * *
const $ = new Env("太平通抽奖");

------------------------------
每天抽奖100次，金币最大损200，自己用的，别拉，测试中.....
------------------------------
"""


import json
import os
import random
import time
import requests

from sendNotify import send

msg = f"\n===== ▷ 抽奖结果 ◁ =====\n"

def lottery(i, token, accessKey, phone, activityCode):
    global msg
    headers = {
        'Host': 'ecustomer.cntaiping.com',
        'Accept': '*/*',
        'x-ac-black-box': 'pWPVg1725333962rb6Teh5r6Yc',
        'channel': '0',
        'Sec-Fetch-Site': 'cross-site',
        'accessKey': accessKey,
        'activityCode': activityCode,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Origin': 'https://ecustomercdn.itaiping.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS',
        'Referer': 'https://ecustomercdn.itaiping.com/',
        'tokenkey': token,
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Content-Type': 'application/json',
    }
    payload = {
        "xCubeActivityCode": activityCode,
        "p_xCubeActivityCode": "andh2008",
        "x_businesskey": "xCubeActivityCode",
        "x_utmId": "11180",
        "x_sourceutmid": "11712",
        "shareCode": ""
    }
    body = json.dumps(payload)
    json_data = {
        'activityCode': activityCode,
        'lotteryMap': {
            'businessInfo': body,
        },
    }
    url = 'https://ecustomer.cntaiping.com/tptplaybox/api/activity/lottery'
    response = requests.post(url, headers=headers, json=json_data)
    response_json = response.json()
    # print(response_json)
    if response_json["errorCode"] == 0:
        prize_name = response_json["value"][0]["showName"]
        message = f'第{i + 1}次 | 获得{prize_name}'
        msg += f'{message}\n'
        print(message)
    else:
        print('抽奖失败')


def lottery_task(token):
    activityCode = 'ngrid2604'
    headers = {
        'Host': 'ecustomer.cntaiping.com',
        'Accept': '*/*',
        'channel': '0',
        'Sec-Fetch-Site': 'cross-site',
        'accessKey': '',
        'activityCode': activityCode,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Origin': 'https://ecustomercdn.itaiping.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;yuangongejia#ios#kehutong#CZBIOS',
        'Referer': 'https://ecustomercdn.itaiping.com/',
        'tokenkey': token,
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Content-Type': 'application/json',
    }
    json_data = {
        'activityCode': activityCode,
        'phone': '',
        'smsCode': '',
        'ticket': '',
        'thirdAccount': token,
        'registerData': {},
    }
    url = 'https://ecustomer.cntaiping.com/tptplaybox/api/account/registerAndLogin'
    response = requests.post(url, headers=headers, json=json_data)
    response_json = response.json()
    if response_json["errorCode"] == 0:
        print("登录成功")
        accessKey = response_json["value"]["accessKey"]
        phone = response_json["value"]["phone"]
        accountId = response_json["value"]["accountId"]

        print(f"【{phone}】开始抽奖......")
        for i in range(100):
            lottery(i, token, accessKey, phone, activityCode)
            time.sleep(random.randint(5, 7))

        # 消息推送
        print(msg)
        send("太平通抽奖", msg)
    else:
        print("登录异常")


if __name__ == '__main__':
    env_name = 'TaiPingTong'
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
        # 第一个账号抽奖
        if i > 1:
            exit(0)
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        token = token_data.get('token')
        user_id = token_data.get('id')
        # 开始任务
        lottery_task(token)

        print("\n随机等待10-15s进行下一个账号")
        time.sleep(random.randint(10, 15))
