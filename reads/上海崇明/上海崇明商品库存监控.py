"""
上海崇明商品库存监控

点击积分兑换进入商品页面，抓商品列表头部token
变量名: SHCMKC_TOKEN

cron: 0 * * * *
const $ = new Env("上海崇明商品库存监控");
"""
import os
import time
import requests
from common import make_request
from sendNotify import send

keywords_to_filter = ['数据线', '徽章', '明信片', '跳绳', '折叠椅', '吊床', '露营车', '帐篷',
                      '帆布包', '笔记本', '手机支架', '漱口水',
                      ]
env_name_kc = 'SHCMKC_TOKEN'
env_name = 'SHCM_TOKEN'
token_kc = os.getenv(env_name_kc)
token = os.getenv(env_name)
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhMDQwYjkwNGM3MGU0ZDcyYjRmYTg3OGVkNmVhYTA0MDZmMjE7MzEwMTUxIiwiaWF0IjoxNzE2ODA3MjU2LCJleHAiOjI3NTM2MDcyNTZ9.xguDe3Kyj9iKk5-Ux6UL7oWfnn5AJNjk284cAbudeauD2xMeUkqu_-_J_5eC0aa4BqIMXcfLqvJMNK-A4oMcoA#0'
token_kc = 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjE3OTUwNDU5NjM2OTk4MTQ0MDEsInN1YiI6InVzZXIiLCJzaXRlIjoiMzEwMTUxIiwiYXJlYVByZWZpeCI6ImNtIiwicm9sZXMiOlsiQlVZRVIiXSwibW9iaWxlIjoiMTc4NTQyNzk1NjUiLCJzaG9wSWQiOiIzMTAxNTEwMSIsImxpdmVNZXNzYWdlIjpudWxsLCJleHAiOjE3MTkzOTkyODIsInV1aWQiOiIxMTZiNjhkYS1hMzI4LTQ4NDktYjFmMy1lZTk0ZDA1NzJlOTYiLCJ1c2VybmFtZSI6Im1lZGlhX2YxN2Y4NWNiIiwidGFyZ2V0IjoibWVkaWEifQ.uicD2O9a3SjeL95gSGocyx1ZOSDEdu7SG6pe4_rjyoJ3ciKaONqCtrx_9-dkITiovAuAukPhuOKN31HPuAfXmQ'
if not token_kc or not token:
    print(f'⛔️未获取到ck变量：请检查变量 {env_name_kc} or {env_name}是否填写')
    exit(0)


def total_score():
    headers = {
        'Host': 'cmapi.shmedia.tech',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'token': '',
        'Content-Type': 'application/json; charset=utf-8',
        'deviceId': 'af223dabdc3b484c8eae7809f6da7ba6',
        'User-Agent': 'StandardApplication/6.2.7 (iPhone; iOS 16.6; Scale/3.00)',
        'Connection': 'keep-alive'
    }
    json_data = {}
    url = 'https://cmapi.shmedia.tech/media-basic-port/api/app/personal/score/total'
    response = make_request(url, json_data, 'post', headers)
    print(response)
    if response and response['code'] == 0:
        return response["data"]["score"]
    else:
        return 0


def can_change_gift():
    msgs = ''
    my_scores = total_score()
    print(f'✅账号当前总积分：{my_scores}')
    print(f'----------------------------')
    # if my_scores <= 0:
    #     return
    mallHeaders = {
        'Host': 'mall-api.shmedia.tech',
        'Authorization': token_kc,
        'Sec-Fetch-Site': 'same-site',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Sec-Fetch-Mode': 'cors',
        'Origin': 'https://mall-mobile.shmedia.tech',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/ChongMing; Version/4.5.4',
        'Referer': 'https://mall-mobile.shmedia.tech/',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Dest': 'empty',
    }
    params = {
        'keyword': '',
        'page_no': '1',
        'page_size': '100',
        'sort': 'create_desc',
        'seller_id': '31015101',
        'shop_cat_id': '1476797667643232258',
    }
    url = 'https://mall-api.shmedia.tech/goods-service/goods/search'
    response = requests.get(url, params=params, headers=mallHeaders)
    if response and response.status_code == 200:
        response_json = response.json()
        gift_list = response_json["data"]
        gift_have_quantity = 0
        for gift in gift_list:
            print(gift)
            goods_id = gift["goods_id"]
            gift_name = gift["name"]
            gift_points = gift["promotion"][0]["exchange"]["exchange_point"]
            # 过滤掉包含关键词的商品
            if any(keyword in gift_name for keyword in keywords_to_filter):
                continue
            enable_quantity = goods_detail(goods_id, mallHeaders)
            msg = f'🐳商品: {gift_name} | 💰积分: {gift_points} | 🐛库存: {enable_quantity}'
            print(msg)
            if enable_quantity > 0:
                gift_have_quantity += 1
                if my_scores >= gift_points:
                    gift_have_quantity = True
                    msgs += msg
                    print(msg)
            time.sleep(3)
        if msgs != '':
            send('上海崇明补库存通知', msgs)
        elif gift_have_quantity > 0:
            print(f'-------------------------------')
            print('😢商品有库存，你积分不足，再等等吧！')
        else:
            print(f'-------------------------------')
            print('😢所有商品均无库存，再等等吧！')


def goods_detail(goods_id, mallHeaders):
    params = {
        'goods_id': goods_id,
    }
    response = requests.get(f'https://mall-api.shmedia.tech/goods-service/goods/{goods_id}/skus', params=params,
                            headers=mallHeaders)
    if response and response.status_code != 200:
        print("获取商品详情异常")
        return
    response_json = response.json()
    goods_name = response_json[0]["goods_name"]
    enable_quantity = response_json[0]["enable_quantity"]

    return enable_quantity


if __name__ == '__main__':
    can_change_gift()
