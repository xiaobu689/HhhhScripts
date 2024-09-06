"""
试玩星

只能 IOS
软件地址：https://fqm001.com/aurora?u=11764664&referer_code=bc87e230cd&v=20240904

抓任意包请求头 cookie
变量名: SWX

cron: 0 0 * * *
const $ = new Env("试玩星");

辅助提醒、自动预约
"""
import os
import random
import re
import time
import requests
from common import get_millisecond_timestamp
from requests.exceptions import RequestException, ProxyError

from sendNotify import send

pushed_ids = []


def game_list(token):
    headers = {
        'Host': 'shiwanxing.com',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': token,
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'cors',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 version=1.2.1 bid=com.depr.haige tk=2',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    }
    ts = get_millisecond_timestamp()
    params = {
        '_uts': '11764664',
        'ts': f'{ts}',
    }
    try:
        response = requests.get('https://shiwanxing.com/s4/lite.subtask.list', params=params, headers=headers,
                                verify=False)
        response.raise_for_status()
        response_json = response.json()
        if response_json['err_code'] != 0:
            print(f'获取任务列表失败|{response_json["err_msg"]}')
            return

        if "操作频率过快" in response_json["err_msg"]:
            print("操作频率过快，请稍后再试")
            return

        payload = response_json['payload']
        tasks = payload['tasks']
        print("tasks=", tasks)
        incoming = payload.get("incoming", [])
        reservation_tasks = payload.get("reservation_tasks", [])

        # 游戏预约
        game_reservation(reservation_tasks, incoming)

        # 游戏通知
        game_notify(tasks)

    except ProxyError as e:
        print(f"代理错误: {e}")
    except RequestException as e:
        print(f"网络请求错误: {e}")
    except ValueError as e:
        print(f"解析JSON出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def game_notify(tasks):
    is_doing = 0
    for item in tasks:
        status = item['status']
        if status == 2:
            is_doing += 1
    if is_doing > 0:
        print("有任务正在执行，稍后再来吧")
    else:
        for item in tasks:
            print(item)
            id = item['id']
            title = item['title']
            qty = item['qty']
            t_mark = item['t_mark']
            if qty > 0 and id not in pushed_ids:
                send_bark_notification("【试玩星】新任务有名额！", title)
                pushed_ids.append(id)


def game_reservation(reservation_tasks, incoming):
    if len(reservation_tasks) == 0:
        for item in incoming:
            id = item['id']
            title = item['title']
            tags = item['tags']
            t_mark = item['t_mark']
            reservation_qty = item['reservation_qty']
            if reservation_qty > 0:
                while True:
                    type = game_reservation_(token, id, t_mark)
                    if type == 2:
                        send("【试玩星】预约成功通知", item)
                        break
    elif len(reservation_tasks) > 0:
        print('已经有预约任务，不可同时预约多个个')


def game_reservation_(token, task_id, t_mark):
    headers = {
        'Host': 'shiwanxing.com',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': token,
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'cors',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 version=1.2.1 bid=com.depr.haige tk=2',
        'Referer': 'https://shiwanxing.com/v4/dashboard',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    }
    ts = get_millisecond_timestamp()
    params = {
        'task_id': task_id,
        't_mark': t_mark,
        'ts': f'{ts}',
    }
    try:
        response = requests.get('https://shiwanxing.com/s5/reservation.acquire', params=params, headers=headers,
                                verify=False)
        response.raise_for_status()
        response_json = response.json()
        if response_json['err_code'] != 0:
            payload = response_json['payload']
            type = payload['type']
            return type
        else:
            return 0
    except ProxyError as e:
        print(f"代理错误: {e}")
        return 0
    except RequestException as e:
        print(f"网络请求错误: {e}")
        return 0
    except ValueError as e:
        print(f"解析JSON出错: {e}")
        return 0
    except Exception as e:
        print(f"发生错误: {e}")
        return 0


def send_bark_notification(title, content):
    env_name = 'BARK_KEYS'
    tokenStr = os.getenv(env_name)
    tokens = re.split(r'@', tokenStr)
    bark_key = tokens[0]
    request_url = f"https://api.day.app/{bark_key}/{title}/{content}"
    response = requests.get(request_url)


if __name__ == '__main__':
    env_name = 'SWX'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    token = tokens[0]
    while True:
        game_list(token)
        time.sleep(random.randint(5, 7))
