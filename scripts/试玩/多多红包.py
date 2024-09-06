"""
多多红包

只能 IOS
软件地址：http://www.ddhb101.store/?r=813566219&d=20240906&en=WearStyle&t=link&m=1&bt=1

抓任意包请求头 cookie
变量名: HBDD

cron: 0 0 * * *
const $ = new Env("多多红包");

辅助提醒
"""

import json
import os
import random
import re
import time
import requests
from requests.exceptions import RequestException, ProxyError

pushed_ids = []


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
        print(response_json)
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
            if quantity:
                send_bark_notification("【红包多多】新任务有名额！", item)
    except ProxyError as e:
        print(f"代理错误: {e}")
    except RequestException as e:
        print(f"网络请求错误: {e}")
    except ValueError as e:
        print(f"解析JSON出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def send_bark_notification(title, content):
    env_name = 'BARK_KEYS'
    tokenStr = os.getenv(env_name)
    tokens = re.split(r'@', tokenStr)
    bark_key = tokens[0]
    request_url = f"https://api.day.app/{bark_key}/{title}/{content}"
    response = requests.get(request_url)


if __name__ == '__main__':
    env_name = 'KFH_TOKEN'
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
            game_list(token)
            time.sleep(random.randint(5, 7))
