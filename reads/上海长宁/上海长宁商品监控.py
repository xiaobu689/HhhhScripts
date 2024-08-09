"""
上海长宁商品库存监控

cron: 0 21 * * *
const $ = new Env("上海长宁商品库存监控");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import make_request, save_result_to_file
from sendNotify import send
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class SHCN():
    name = "上海长宁商场库存监控"

    def __init__(self, account_info):
        self.token = account_info.split('#')[0]
        self.verify = False
        self.total_scores = 0
        self.headers = {
            'Host': 'cnapi.shmedia.tech',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'token': self.token,
            'Content-Type': 'application/json; charset=utf-8',
            'deviceId': 'af223dabdc3b484c8eae7809f6da7ba6',
            'User-Agent': 'StandardApplication/6.2.7 (iPhone; iOS 16.6; Scale/3.00)',
            'Connection': 'keep-alive'
        }
        self.mallHeaders = {
            'Host': 'mall-api.shmedia.tech',
            'Authorization': '',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://mall-mobile.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148Rmt/ChangNing; Version/6.2.8',
            'Connection': 'keep-alive',
            'Referer': 'https://mall-mobile.shmedia.tech/',
            'Sec-Fetch-Dest': 'empty'
        }

    def total_score(self):
        json_data = {}
        url = 'https://cnapi.shmedia.tech/media-basic-port/api/app/personal/score/total'
        response = make_request(url, json_data, 'post', self.headers)
        if response and response['code'] == 0:
            total_scores = response["data"]["score"]
            self.total_scores = total_scores
            print(f'✅账号当前总积分：{total_scores}')
        else:
            print(f'❌总积分获取失败：{response}')

    def mall_login(self):
        headers = {
            'Host': 'mall-api.shmedia.tech',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': 'https://mall-mobile.shmedia.tech',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148Rmt/ChangNing; Version/6.2.8',
            'Referer': 'https://mall-mobile.shmedia.tech/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty'
        }
        data = {
            'siteId': '310105',
            'token': self.token,
            'target': 'media',
        }
        url = 'https://mall-api.shmedia.tech/member-service/passport/media/app/login'
        response = requests.post(url, headers=headers, data=data)
        if not response or response.status_code != 200:
            print("商场登录失败")
            save_result_to_file("error", self.name)
            return
        else:
            response_json = response.json()
            mobile = response_json["mobile"]
            access_token = response_json["access_token"]
            self.mallHeaders['Authorization'] = access_token
            save_result_to_file("success", self.name)
            print(f'✅商场登录成功：{mobile}')


    def can_change_gift(self):
        print(f"\n======== ▷ 商品列表 ◁ ========")
        msgs = ''
        all_gift_list = []
        keywords_to_filter = ['帆布袋', 'U盘', '折叠伞', '笔记本', '惠润']
        if int(self.total_scores) <= 0:
            return
        shop_cat_ids = ['1473187237167882242', '1473187292704661505']
        for shop_cat_id in shop_cat_ids:
            params = {
                'seller_id': '31010501',
                'page_no': '1',
                'page_size': '100',
                'shop_cat_id': shop_cat_id,
                'sort': 'create_desc',
            }
            url = 'https://mall-api.shmedia.tech/goods-service/goods/search'
            response = requests.get(url, params=params, headers=self.mallHeaders)
            if response and response.status_code == 200:
                response_json = response.json()
                gift_list = response_json["data"]
                all_gift_list.extend(gift_list)
        gift_have_quantity = 0
        for gift in all_gift_list:
            goods_id = gift["goods_id"]
            gift_name = gift["name"]
            gift_points = gift["promotion"][0]["exchange"]["exchange_point"]
            if any(keyword in gift_name for keyword in keywords_to_filter):
                continue
            enable_quantity = self.goods_detail(goods_id)
            msg = f'🐳|{gift_name} | 积分: {gift_points} | 库存: {enable_quantity}'
            print(msg)
            if enable_quantity > 0:
                gift_have_quantity += 1
                if int(self.total_scores) >= gift_points:
                    gift_have_quantity = True
                    msgs += msg
                    print(msg)
        print(f"\n======== ▷ 可兑换商品列表 ◁ ========")
        if msgs != '' and int(self.total_scores) >= 10000:
            print("达标提醒：积分已满10000")
            # send('上海长宁商品库存监控', msgs)
        elif gift_have_quantity > 0:
            print('😢商品有库存，你积分不足，再等等吧！')
        else:
            print('😢所有商品均无库存，再等等吧！')

    def goods_detail(self, goods_id):
        params = {
            'goods_id': goods_id,
        }
        url = f'https://mall-api.shmedia.tech/goods-service/goods/{goods_id}/skus'
        response = requests.get(url, params=params, headers=self.mallHeaders)
        if response and response.status_code != 200:
            print("获取商品详情异常")
            return
        response_json = response.json()
        goods_name = response_json[0]["goods_name"]
        enable_quantity = response_json[0]["enable_quantity"]

        return enable_quantity

    def main(self):
        self.total_score()
        self.mall_login()
        self.can_change_gift()


if __name__ == '__main__':
    env_name = 'SHCN_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"上海长宁商场共获取到{len(tokens)}个账号")
    for i, account_info in enumerate(tokens, start=1):
        if i == 1:
            print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
            SHCN(account_info).main()
            print("\n随机等待30-60s进行下一个账号")
            time.sleep(random.randint(10, 15))


