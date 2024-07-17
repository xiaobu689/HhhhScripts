"""
上海杨浦商品库存监控

点击积分兑换进入商品页面，抓商品列表头部token
变量名: SHYPKC_TOKEN

cron: */55 * * * *
const $ = new Env("上海杨浦商品库存监控");
"""
import os
import time
import requests
from common import make_request
from sendNotify import send

keywords_to_filter = ['数据线', '徽章', '明信片', '跳绳', '折叠椅', '吊床', '露营车', '帐篷',
                      '帆布包', '笔记本', '手机支架', '漱口水',
                      ]
env_name_kc = 'SHYPKC_TOKEN'
env_name = 'SHYP_TOKEN'
token_kc = os.getenv(env_name_kc)
token = os.getenv(env_name)
if not token_kc or not token:
    print(f'⛔️未获取到ck变量：请检查变量 {env_name_kc} or {env_name}是否填写')
    exit(0)

headers = {
    'Host': 'ypapi.shmedia.tech',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-Hans-CN;q=1',
    'token': token.split('#')[0],
    'Content-Type': 'application/json; charset=utf-8',
    'deviceId': 'af223dabdc3b484c8eae7809f6da7ba6',
    'User-Agent': 'StandardApplication/6.2.7 (iPhone; iOS 16.6; Scale/3.00)',
    'Connection': 'keep-alive'
}

mallHeaders = {
    'Host': 'mall-api.shmedia.tech',
    'Authorization': token_kc,
    'Sec-Fetch-Site': 'same-site',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Sec-Fetch-Mode': 'cors',
    'Origin': 'https://mall-mobile.shmedia.tech',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148Rmt/BaoShan; Version/2.3.8',
    'Referer': 'https://mall-mobile.shmedia.tech/',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Dest': 'empty',
}


def total_score():
    json_data = {}
    url = 'https://ypapi.shmedia.tech/media-basic-port/api/app/personal/score/total'
    response = requests.post(url, headers=headers, json=json_data, )
    if not response or response.status_code != 200:
        return
    response_json = response.json()
    if response_json['code'] == 0:
        return response_json["data"]["score"]
    else:
        return 0


def can_change_gift():
    msgs = ''
    my_scores = total_score()
    print(f'✅账号当前总积分：{my_scores}')
    print(f'----------------------------')
    if my_scores <= 0:
        return
    # 生活百货
    params_1 = {
        'seller_id': '31011001',
        'page_no': '1',
        'page_size': '10',
        'shop_cat_id': '1391586488730075138',
        'sort': 'create_desc',
    }
    response_1 = requests.get('https://mall-api.shmedia.tech/goods-service/goods/search', params=params_1,
                              headers=mallHeaders).json()
    # 虚拟产品
    params_2 = {
        'seller_id': '31011001',
        'page_no': '1',
        'page_size': '10',
        'shop_cat_id': '1431136756879056898',
        'sort': 'create_desc',
    }
    response_2 = requests.get('https://mall-api.shmedia.tech/goods-service/goods/search', params=params_2,
                              headers=mallHeaders).json()
    # 限时福利
    params_3 = {
        'seller_id': '31011001',
        'page_no': '1',
        'page_size': '10',
        'shop_cat_id': '1544652237932859394',
        'sort': 'create_desc',
    }
    response_3 = requests.get('https://mall-api.shmedia.tech/goods-service/goods/search', params=params_3,
                              headers=mallHeaders).json()
    # 数码电子
    params_4 = {
        'seller_id': '31011001',
        'page_no': '1',
        'page_size': '10',
        'shop_cat_id': '1386875324743868488',
        'sort': 'create_desc',
    }
    response_4 = requests.get('https://mall-api.shmedia.tech/goods-service/goods/search', params=params_4,
                              headers=mallHeaders).json()
    gift_list = response_1['data'] + response_2['data'] + response_3['data'] + response_4['data']
    gift_have_quantity = 0
    for gift in gift_list:
        goods_id = gift["goods_id"]
        gift_name = gift["name"]
        gift_points = gift["promotion"][0]["exchange"]["exchange_point"]
        # 过滤掉包含关键词的商品
        if any(keyword in gift_name for keyword in keywords_to_filter):
            continue
        enable_quantity = goods_detail(goods_id)
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
        print(f'--------------当前可兑换-----------------')
        print(msgs)
        send('上海杨浦补库存通知', msgs)
    elif gift_have_quantity > 0:
        print(f'-------------------------------')
        print('😢商品有库存，你积分不足，再等等吧！')
    else:
        print(f'-------------------------------')
        print('😢所有商品均无库存，再等等吧！')


def goods_detail(goods_id):
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
