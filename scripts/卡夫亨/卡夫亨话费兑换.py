"""
卡夫亨话费兑换

cron: */15 * * * *
const $ = new Env("卡夫亨话费兑换");
"""


import json
import os
import requests
from sendNotify import send

phone = ''
score = 0
memberId = 0

def user_info(token):
    headers = {
        'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'token': token,
        'Origin': 'https://fscrm.kraftheinz.net.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x1800323d) NetType/4G Language/zh_CN',
        'Referer': 'https://fscrm.kraftheinz.net.cn/',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Dest': 'empty',
    }
    url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/getUserInfo'
    response_json = requests.get(url, headers=headers).json()
    if response_json['error_code'] == 0:
        global memberId, phone, score
        memberId = response_json['data']['member_id']
        phone = response_json['data']['memberInfo']['phone']
        score = response_json['data']['memberInfo']['score']
        print(f'账号:{memberId} | 手机: {phone} | 积分:{score}')
        return True
    else:
        return False


def exchange(token):
    headers = {
        'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'token': token,
        'Origin': 'https://fscrm.kraftheinz.net.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x1800323d) NetType/4G Language/zh_CN',
        'Referer': 'https://fscrm.kraftheinz.net.cn/',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Dest': 'empty',
    }
    if score < 100:
        print(f'积分不足,当前积分为:{score}/100, 兑换取消！')
        return
    data = {
        'value': '全网10元话费',
        'phone': phone,
        'type': '话费',
        'memberId': memberId,
    }
    url = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/exchangeIntegralNew'
    response_json = requests.post(url, headers=headers, data=data).json()
    if response_json['error_code'] == 0:
        content = f'账号:{phone}兑换10元话费成功！'
        print(content)
        send('卡夫亨积分兑换通知', content)
    else:
        print('兑换失败')


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
        token = token_data.get('token')
        user_id = token_data.get('id')
        print(token)
        if user_info(token):
            exchange(token)
        break
