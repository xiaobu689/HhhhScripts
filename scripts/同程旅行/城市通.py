"""
城市通

* 每日视频 | 30积分，地铁抵扣0.3元 | 可叠加
* 每日签到领里程
* 400里程兑2元地铁券 | 每日1次
* 100里程兑换1元地铁券 | 每周一次

--------------------------
20240708 支持多账号功能，增加每周一次五折兑换
20240627 增加每天兑换地铁券功能，一天一次
20240616 金币任务，暂时没啥兑的，活动入口也突然消失了，金币可正常增加，防内测，暂时不做
20240614 自己坐地铁用的，没啥毛，没做封装提取，别拉取，仅适合自己使用
20240808 更新脚本，添加部分浏览任务，移除部分已废任务
--------------------------

抓任意包请求头 TC-MALL-USER-TOKEN
变量名: CST_TOKEN
格式：
[
    {
        "id": "随意，微信名",
        "token": "ohmxxxxxdTGVU",
        "deptCode": "iH3PkxxxxxeylA==",
        "appId": "wx622xxxxf7008",
        "openId": "o4VjT5AxxxxxCjVDBpRd0",
        "unionId": "ohmdTtxxxx1U2DGcZmGVU"
    }
]
cron: 35 5 * * *
const $ = new Env("城市通");
"""
import datetime
import json
import os
import random
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import make_request, get_current_timestamp_milliseconds, save_result_to_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class CST():
    name = "城市通"

    def __init__(self, token_data):
        self.cityCode = '310000'
        self.userName = token_data.get('id')
        self.token = token_data.get('token')
        self.appId = token_data.get('appId')
        self.openId = token_data.get('openId')
        self.unionId = token_data.get('unionId')
        self.deptCode = token_data.get('deptCode')
        self.UA = f'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003131) NetType/4G Language/zh_CN miniProgram/{self.appId}'
        self.verify = False
        self.totalScore = 0
        self.activityCode = ''
        self.taskCode = ''
        self.recordNo = ''
        self.coinTaskCode = ''
        self.coinRecordNo = ''
        self.headers = {
            'Host': 'tcmobileapi.17usoft.com',
            'TC-MALL-PLATFORM-CODE': 'SUBWAY_MP',
            'TC-MALL-OS-TYPE': 'IOS',
            'TC-MALL-DEPT-CODE': self.deptCode,
            'Origin': 'https://wx.17u.cn',
            'User-Agent': self.UA,
            'TC-MALL-CLIENT': 'API_CLIENT',
            'TC-MALL-USER-TOKEN': self.token,
            'TC-MALL-PLATFORM-SUB': 'SUBWAY_MP'
        }
        self.signHeaders = {
            'Host': 'wx.17u.cn',
            'TC-MALL-USER-TOKEN': self.token,
            'User-Agent': self.UA,
            'TC-MALL-PLATFORM-SUB': 'SUBWAY_MP',
            'TC-MALL-PLATFORM-CODE': 'SUBWAY_MP',
            'TC-MALL-DEPT-CODE': self.deptCode,
            'Origin': 'https://wx.17u.cn',
            'TC-MALL-OS-TYPE': 'IOS'
        }
        self.taskHeaders = {
            'Host': 'cvg.17usoft.com',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Labrador-Token': '6ee05193-0f17-47ec-9965-f2bc713b9b3b',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': self.UA
        }

    def sign(self):
        json_data = {}
        url = 'https://wx.17u.cn/wxmpsign/sign/saveSignInfo'
        response = requests.post(url, headers=self.signHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'✅签到成功')
            else:
                print(f'✅签到成功， {response_json["msg"]}')
        else:
            print(f'❌签到失败')

    def user_mileage_info(self):
        json_data = {}
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/userApi/mileages/remain'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                save_result_to_file("success", self.name)
                balance = response_json["data"]["remainMileageTitle"]
                self.totalScore = balance
                print(
                    f'🐶账号: {self.userName} | ✅当前可用里程：{balance} | 💰价值：{response_json["data"]["deductionPrice"]}元')
            else:
                save_result_to_file("error", self.name)
        else:
            save_result_to_file("error", self.name)

    def daily_task(self):
        traceId = get_current_timestamp_milliseconds()
        json_data = {
            'deviceSystem': 'ios',
            'appId': self.appId,
            'cityCode': self.cityCode,
            'channelCode': 'defaultChannel',
            'traceId': traceId,
            'activityKey': 'sqzq_rw',
            'openId': self.openId,
            'unionId': self.unionId,
            'supplier': 'SH_SHS_M',
            'supplierId': self.cityCode,
            'sign': '619fdd6180f41f6bbe6087713eb7fab',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/userQueryTaskList'
        response = make_request(url, json_data=json_data, method='post', headers=self.taskHeaders)
        # print(response)
        if response and response["code"] == 1000:
            activityCode = response["data"]["activityCode"]
            self.activityCode = activityCode
            tasks = response["data"]["detailsList"]
            for task in tasks:
                main_title = task["mainTitle"]
                task_code = task["taskCode"]
                if task_code in ["TAS_6645F56080A21CDU80", "TAS_66AAFUA880C7D1A198", "TAS_6645CC9880A20B2DD1",
                                 "TAS_66AB312370C7F20BB2"]:
                    continue
                if task["state"] == 3:
                    print(f'✅任务已完成 | {task_code} | {main_title}')
                else:
                    # 做任务
                    print(f'🌼开始任务 | {task_code} | {main_title}')
                    self.taskCode = task_code
                    if task["recordNo"] != "":
                        self.recordNo = task["recordNo"]

                    # 领取任务
                    self.receive_task()
                    time.sleep(random.randint(10, 15))

                    # 完成任务
                    i = 0
                    if self.taskCode == "TAS_6645F68A70A21U4C23" or self.taskCode == "TAS_66B48FFF80CC6AA9UC":
                        i = 5
                    else:
                        i = 1
                    for i in range(i):
                        self.complete_task()
                        time.sleep(random.randint(10, 15))

                    # 领取奖励
                    self.receive_rewards()
                    time.sleep(random.randint(10, 15))

    def receive_task(self):
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'share_rf_cxxc_240524',
            'traceId': 1718207195210,
            'activityCode': 'ACT_6645F6UF80A21F1BD0',
            'taskCode': self.taskCode,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '02b4bc7c82826a2e88403a363ca92345',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/receiveTask'
        response = requests.post(url, headers=self.taskHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 1000:
                self.recordNo = response_json['data']['recordNo']
                print(f'✅任务领取成功 | 任务ID: {self.recordNo}')

    def complete_task(self):
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'share_rf_cxxc_240524',
            'traceId': 1718207232790,
            'recordNo': self.recordNo,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': 'd7071de3ec0c8cf506b217191d6b6b74',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/completeTask'
        response = requests.post(url, headers=self.taskHeaders, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                print(f'✅任务完成')
            else:
                print(f'❌任务失败')

    def receive_rewards(self):
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'defaultChannel',
            'traceId': 1717438573341,
            'recordNo': self.recordNo,
            'activityCode': 'ACT_6645F6UF80A21F1BD0',
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '5b75aeb5b8abbd33d778da7548f9d1f5',
        }
        url = 'https://cvg.17usoft.com/marketingbff/saveMoneyZone/receiveAward'
        response = make_request(url, json_data=json_data, method='post', headers=self.taskHeaders)
        if response and response["code"] == 1000:
            print(
                f'✅金币领取成功 | 金币：{response["data"]["awardAmount"]} | 价值：{response["data"]["awardDeductionAmount"]}元')
        else:
            print(f'❌领取失败')

    def coin_task(self):
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '12d1fab944be9b6543366820de5ab3a9',
        }
        response = requests.post('https://cvg.17usoft.com/cst/activity/center/activity/taskFlow',
                                 headers=self.taskHeaders,
                                 json=json_data)
        # 检查是否有响应
        if not response or response.status_code != 200:
            print("response err")
            return

        response_json = response.json()
        if response_json and response_json["code"] == 1000:
            tasks = response_json["result"]["taskList"]
            for task in tasks:
                taskCode = task["taskCode"]
                if task["taskName"] == "CST会员看视频任务":
                    print(f'\n🐶开始视频观看任务......')
                    for i in range(10):
                        coinRecordNo = self.coin_task_complate(taskCode)
                        time.sleep(random.randint(30, 40))
                        self.coin_task_receive(taskCode, coinRecordNo)
                        time.sleep(random.randint(15, 20))
                elif task["taskName"] == "CST会员公交订单任务":
                    print("\n🐱开始公交订单任务......")
                    coinRecordNo = self.coin_task_complate(taskCode)
                    time.sleep(random.randint(30, 40))
                    self.coin_task_receive(taskCode, coinRecordNo)
                    time.sleep(random.randint(30, 40))

                elif task["taskName"] == "CST会员抽奖任务":
                    print("\n🐹开始抽奖任务......")
                    # 金币抽奖
                    response_json = self.lucky_draw()
                    time.sleep(random.randint(30, 40))
                    self.lucky_draw_receive(response_json)
                    time.sleep(random.randint(30, 40))
                    # 领取任务完成奖励
                    coinRecordNo = self.coin_task_complate(taskCode)
                    time.sleep(random.randint(30, 40))
                    self.coin_task_receive(taskCode, coinRecordNo)
                    time.sleep(random.randint(30, 40))

                elif task["taskName"] == "CST会员酒店浏览任务":
                    print("\n✈️开始浏览任务......")
                    coinRecordNo = self.coin_task_complate(taskCode)
                    time.sleep(random.randint(30, 40))
                    self.coin_task_receive(taskCode, coinRecordNo)
                    time.sleep(random.randint(30, 40))
        else:
            return

    def coin_task_complate(self, taskCode):
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'taskCode': taskCode,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': 'f0026697d9f03b6075496aacb4728011',
        }
        response = requests.post(
            'https://cvg.17usoft.com/cst/activity/center/activity/dailyTaskRecAndFinish',
            headers=self.taskHeaders,
            json=json_data,
        )
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                recordNo = response_json["result"]["recordNo"]
                return recordNo
            else:
                return None
        else:
            return None

    def coin_task_receive(self, coinTaskCode, coinRecordNo):
        json_data = {
            'deviceSystem': 'ios',
            'appId': 'wx624dc2cce62f7008',
            'cityCode': '310000',
            'channelCode': 'sqzq',
            'taskCode': coinTaskCode,
            'recordNo': coinRecordNo,
            'openId': 'o4VjT5Az0RxdUIz6-sBCjVDBpRd0',
            'unionId': 'ohmdTt1TSce70l1uL1U2DGcZmGVU',
            'supplier': 'SH_SHS_M',
            'supplierId': '310000',
            'sign': '005ea39bf4dc469ce95a38b4fc2e4744',
        }

        response = requests.post(
            'https://cvg.17usoft.com/cst/activity/center/activity/dailyTaskSendCoin',
            headers=self.taskHeaders,
            json=json_data,
        )
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json and response_json["code"] == 1000:
                print(f'✅{response_json["result"]["recordNo"]} | 任务完成 | 奖励领取完成')

    # 100金币兑换1元地铁券，一周一次
    def weekly_coupon_exchange(self):
        params = {
            'zoneId': '8',
        }
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/activityApi/superCoupon/zoneSku'
        response = requests.get(url, params=params, headers=self.headers)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                coupons = response_json['data']["skuInfos"]
                for coupon in coupons:
                    if coupon["baseInfo"]["threeLevelCategoryName"] != "公交地铁":
                        continue
                    status = coupon["buttonInfo"]["content"]
                    skuPriceId = coupon["saleInfo"]["skuPriceId"]
                    salePrice = coupon["saleInfo"]["salePrice"]
                    skuId = coupon["baseInfo"]["skuId"]
                    print(f'✅{coupon["baseInfo"]["skuTitle"]} | {status}')
                    if status == "已兑换":
                        print("1元地铁券本周已兑换，下周再来")
                        continue
                    # 兑换1元地铁券
                    self.exchange_100(skuPriceId, salePrice, skuId)

    def exchange_100(self, skuPriceId, salePrice, skuId):
        json_data = {
            'salePrice': salePrice,
            'skuId': skuId,
            'skuPriceId': skuPriceId,
            'zoneId': 8,
            'refId': 0,
            'channelCode': 'superCoupon',
        }
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/activityApi/superCoupon/submitOrder'
        response_json = requests.post(url, headers=self.headers, json=json_data).json()
        if response_json["code"] == 200:
            print(f'✅地铁券兑换|1元券--100积分 | 兑换成功')
        else:
            print(f'❌地铁券兑换|1元券--100积分 | 兑换失败')

    # 400积分兑换2元地铁券
    def exchange_400(self, total_score):
        if int(total_score) < 400:
            print(f'⛔️积分不足400，无法兑换地铁券')
            return
        json_data = {
            'salePrice': '400',
            'skuId': '40750',
            'refId': 2000027364,
            'channelCode': 'couponExchange.3-40',
        }
        url = 'https://tcmobileapi.17usoft.com/mallgatewayapi/orderApi/externalOrder/submitOrder'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            print(f'兑换失败')
            return
        response_json = response.json()
        if response_json and response_json["code"] == 200:
            print(f'兑换成功 | {response_json["data"]["message"]}')
        else:
            print(f'兑换失败 | {response_json["data"]["message"]}')

    def main(self):
        self.user_mileage_info()

        # 签到
        self.sign()
        time.sleep(random.randint(10, 15))

        # 日常任务
        self.daily_task()
        time.sleep(random.randint(10, 15))

        # 领金币任务、看视频
        # self.coin_task()

        # 100积分兑换1元地铁券
        self.weekly_coupon_exchange()
        time.sleep(random.randint(5, 10))

        # 400积分兑换2元地铁券
        # self.exchange_400(self.totalScore)]
        # time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    env_name = 'CST_TOKEN'
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
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        CST(token_data).main()
        print("\n随机等待10-15s进行下一个账号")
        time.sleep(random.randint(10, 15))
