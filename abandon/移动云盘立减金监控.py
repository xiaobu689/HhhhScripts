"""
【临时】移动云盘美图秀秀立减金监控

cron: 30 8 * * *
const $ = new Env("【临时】移动云盘美图秀秀立减金监控");
"""

exit(0)

import os
import random
import time
import requests

from sendNotify import send

send_count = 0


def get_cash_remaining():
    global send_count
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '',
        'priority': 'u=1, i',
        'referer': 'https://caiyun.feixin.10086.cn:7071/portal/cloudCircle/index.html?path=backupMeitu&sourceid=1000&enableShare=1&token=',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    params = {
        'marketName': 'National_BackupMeitu',
    }

    response = requests.get(
        'https://caiyun.feixin.10086.cn:7071/market/prize/prizepool/list',
        params=params,
        headers=headers,
    )

    response_json = response.json()
    if response_json['code'] == 0:
        list = response_json['result']
        for item in list:
            prizeName = item['prizeName']
            dailyRemainderCount = item['dailyRemainderCount']
            dailyCount = item['dailyCount']
            if prizeName == "5元微信立减金" or prizeName == '5元支付宝红包':
                if dailyRemainderCount > 0:
                    print(f'微信立减金|支付宝红包有库存')
                    # 只推送3次消息
                    if send_count < 3:
                        send(f'{prizeName}补库存通知', f'{prizeName} | 当前剩余{dailyRemainderCount}/{dailyCount}')
                        send_count += 1
    else:
        print(f'奖品列表获取失败')


if __name__ == '__main__':
    while True:
        get_cash_remaining()
        time.sleep(random.randint(10, 15))
