"""
多多红包

只能 IOS
软件地址：http://www.ddhb101.store/?r=813566219&d=20240906&en=WearStyle&t=link&m=1&bt=1

抓任意包请求头 cookie
变量名: HBDD

cron: 30 8 * * *
const $ = new Env("多多红包");

辅助提醒
"""

import json
import os
import random
import requests
from requests.exceptions import RequestException, ProxyError
import os
import re
import time
from datetime import datetime
from sendNotify import send

pushed_ids = []


# 任务通知
def game_list(token):
    headers = {
        'Host': 'api.duoduo365.com',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Site': 'same-site',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.duoduo365.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PPhongbao/6.6.0 ssl',
        'Referer': 'https://www.duoduo365.com/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': token,
    }
    params = {
        'type': '1',
    }
    data = {
        'accnew': 'V1JQAAFQBFteUQFdDw==',
        't': '1725547884589',
    }
    try:
        response = requests.post(
            'https://api.duoduo365.com/fasttask/getTaskList',
            params=params,
            headers=headers,
            data=data,
        )
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] != 10000:
            print(f'获取任务列表失败')
            return
        taskList = response_json['taskList']
        is_reserved = response_json['is_reserved']
        if is_reserved:
            print("已有试玩在进行中")
            return
        for item in taskList:
            name = item['name']
            if name == '邀请赚钱' or name == '浏览30秒视频广告':
                continue
            id = item['id']
            amount = item['amount']
            quantity = item['quantity']
            name = item['name']
            if quantity:
                print(f'【红包多多】新任务有名额！| {name}')
                send_bark_notification("【红包多多】新任务有名额！", name)
    except ProxyError as e:
        print(f"代理错误: {e}")
    except RequestException as e:
        print(f"网络请求错误: {e}")
    except ValueError as e:
        print(f"解析JSON出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 预约通知
def game_reservation(token):
    headers = {
        'Host': 'api.duoduo365.com',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Site': 'same-site',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.duoduo365.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PPhongbao/6.6.0 ssl',
        'Referer': 'https://www.duoduo365.com/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': token,
    }
    params = {
        'type': '3',
    }
    data = {
        'accnew': 'V1JQAA1QAVFTVgddDg==',
        't': '1725942253388',
    }
    response = requests.post(
        'https://api.duoduo365.com/fasttask/getTaskList',
        params=params,
        headers=headers,
        data=data,
    )
    response_json = response.json()
    if response_json['code'] != 10000:
        print(f'获取预约列表失败')
        return
    subscribe_list = response_json['subscribe_list']
    if len(subscribe_list) > 0:
        print("已有预约任务")
        return
    taskList = response_json['taskList']
    for item in taskList:
        id = item['id']
        amount = item['amount']
        tags = item['tags']
        img_name = item['img_name']
        for tag in tags:
            if tag == '可预约':
                content = f'{id}|{amount}元|{img_name}'
                send_bark_notification("【红包多多】新任务可预约！", content)


def game_task(token):
    game_list(token)
    game_reservation(token)


def send_bark_notification(title, content):
    env_name = 'BARK_KEYS'
    tokenStr = os.getenv(env_name)
    tokens = re.split(r'@', tokenStr)
    bark_key = tokens[0]
    print(bark_key)
    request_url = f"https://api.day.app/{bark_key}/{title}/{content}"
    response = requests.get(request_url)
    print(response.text)


if __name__ == '__main__':
    env_name = 'HBDD'
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
        if i > 1:
            continue
        token = token_data.get('token')
        user_id = token_data.get('id')
        while True:
            now = datetime.now()
            if now.hour in [21]:
                break

            game_task(token)
            time.sleep(random.randint(6, 8))
