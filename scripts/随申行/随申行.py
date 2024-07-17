"""
随申行


路径：随申行APP
用途：签到、做任务、养宠物攒兜豆，兑换上海地铁优惠券
变量名：SSX_COOKIE
格式： 任意请求头抓 Authorization 值

---------------------------------
20240610 新增每日签到、浏览商场任务
20240601 抽奖活动下线移除
20240529 新增当日首次登陆、游戏成就分享
---------------------------------
定时设置：每天1次，时间随意
cron: 0 0 * * *
const $ = new Env("随申行");
"""
import os
import random
import time
import requests
from datetime import datetime
from common import make_request, save_result_to_file
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import qianwen_messages
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from sendNotify import send


class SSX():
    name = "随申行"

    def __init__(self, cookie):
        parts = cookie.split('#')
        self.cookie = parts[0]
        self.uid = parts[1]
        self.adoptingId = 0
        self.adoptingName = ''
        self.needReceiveBean = 0
        self.msg = ''
        self.gpsHeaders = {
            'Host': 'dualstack-restios.amap.com',
            'Accept': '*/*',
            'platinfo': 'platform=iOS&product=sea&sdkversion=9.7.0&founversion=1.8.2',
            'x-info': 't34+94jruh/r2BCfvOVOAdT/3hBBx5N7L2rs2wkhydqjoBoMlswtRSzEnP4GoLbT1Pb8820nK8KarglxuCo0RYIQ6/W6+rsH5iJe6Qr3E+jwqcYJDRRhP2uhUUrEKSc0UTaCX5J8CricuFCAcVl+8vqP7xkEJObHQqeNqYd7d1INtIxMjY0YDRkNWP1LMlKLGA0YBCwtrCzNrZKTrYwtrEytjE0ZGDgMgPpAAM5gkMPvWpvM3MRk25qkzBTb5Dy94ozcxMRiPRBRU1ySX5SYnmpraGRoaWxYU5SYa2tqZmlak1iUnGHrGORrZuIKAGfGhIoKAQAA',
            'logversion': '2.1',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'AMAP_SDK_iOS_Search_9.7.0',
            'Connection': 'keep-alive',
            'csid': '6C593DEE-6628-4EFB-999E-010569620BBB'
        }
        self.headers = {
            'Host': 'api.shmaas.net',
            'User-Agent': 'ios-shell-maas/2.00.41 (iPhone; iOS 16.6; Scale/3.00)',
            'X-Saic-App-Version': '2.00.41',
            'X-Saic-Req-Ts': '1716953610832',
            'X-Saic-LocationTime': '1716953604744',
            'X-Maas-Req-Ts': '1716953610830.563965',
            'X-Saic-Real-App-Version': '2.00.41.27141',
            'X-Saic-Channel': 'maas',
            'X-Saic-AppId': 'maas_car',
            'X-Saic-Gps': '121.306501,31.136068',
            'X-Saic-Device-Id': '633EB41D5EEC41B1BA90E94C0A37D1D6',
            'X-Saic-OS-Name': 'ios',
            'X-Saic-User-Agent': 'timezone/GMT+8 platform/iOS platform_version/16.6 carrier_code/65535 carrier_name/-- device_name/iPhone device_id/633EB41D5EEC41B1BA90E94C0A37D1D6 app_name/passenger app_version/2.00.41',
            'X-Saic-Platform': 'IOS',
            'X-Saic-Finger': '5503748B-E81C-45B9-AA30-326F15A40C91',
            'X-Saic-ProductId': '5',
            'X-Saic-CityCode': '310100',
            'Connection': 'keep-alive',
            'X-Saic-Ds': 'db0cdc011b62592d',
            'uid': self.uid,
            'Authorization': self.cookie,
            'Accept-Language': 'zh-Hans-CN;q=1',
            'X-Saic-Req-Sn': 'EAFB3547-C4EB-4078-8C4F-66405E351E08',
            'env': 'release',
            'X-Saic-Location-CityCode': '310100',
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'X-Maas-Req-Sn': '8C4EACA9-06DD-4FAF-8CFA-1D6657F2FE68',
            'X-Saic-LocationAccuracy': '28.780395'
        }

    def getUserInfo(self):
        json_data = {
            'clientId': '1501489616703070208',
            'language': 'zh-cn',
        }
        url = 'https://api.shmaas.net/auth/maas/queryUserInformationForPersonalCenter'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['errCode'] == 0:
            save_result_to_file("success", self.name)
            msg = f'---------------------------\n'
            msg += f'🐹昵称：{response["data"]["userBasicInformation"]["name"]}\n'
            msg += f'🐹手机：{response["data"]["userBasicInformation"]["mobile"]}\n'
            msg += f'🐹兜豆：{response["data"]["userCombineInformation"]["userCredit"]["greenCredit"]}'

            self.msg += msg
            print(msg)
        else:
            save_result_to_file("error", self.name)

    def receive(self):
        url = 'https://api.shmaas.net/cap/base/platform/receiveBubbleCredit'
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "greenCreditTime": current_time,
            "language": "zh-cn",
            "carBonTypeName": "任务",
            "uniqueId": f"任务_{self.needReceiveBean}_{current_time}",
            "greenCredit": self.needReceiveBean
        }
        msg = f'-----------------------------------\n'
        response = requests.post(url, headers=self.headers, json=data).json()
        if response['errCode'] == 0:
            msg += f'✅今日兜豆奖励领取成功！\n'
            print(msg)
        elif response['errCode'] == -2763132:
            msg += f'❌已经领取过了，请勿重复领取！\n'
            print(msg)
        else:
            msg += f'❌领取失败， cookie可能已失效：{response["errMsg"]}\n'
            print(msg)

    def task_list(self):
        url = 'https://api.shmaas.net/cap/app/queryLowCarbonHome'
        data = {"language": "zh-cn"}
        response = requests.post(url, headers=self.headers, json=data).json()
        if response['errCode'] == 0:
            # 获取正在喂养的宠物ID, adoptionValue: 1喂养完成 2喂养中
            for i in response['data']['userGames']:
                if i["adoptionValue"] == 2:
                    self.adoptingName = i["gameName"]
                    break
            msg = f'\n---------- 🐹任务列表🐹 ----------\n'
            for i in response['data']['userActivityMessages']:
                if "用户注册" in i["name"] or "用户实名" in i["name"] or "用户首单" in i["name"] or "打车出行" in i[
                    "name"]:
                    continue
                msg += f'✅{i["name"]}: {"已完成" if i["finishStatus"] == 1 else "未完成"}\n'
        else:
            msg = f'❌获取任务列表信息失败， cookie可能失效：{response["errMsg"]}'

        self.msg += msg
        print(msg)

    def user_game_list(self):
        json_data = {
            'language': 'zh-cn',
        }
        url = 'https://api.shmaas.net/cap/base/credits/v2/queryUserGameList'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['errCode'] == 0:
            for i in response['data']['gameCardInfo']:
                if i["type"] == 2:  # type 2喂养中
                    self.adoptingId = i["gameId"]
                    break

    def get_game_info(self):
        msg = ''
        url = 'https://api.shmaas.net/cap/base/credits/queryNowAdoptInfo'
        data = {"language": "zh-cn"}
        response = requests.post(url, headers=self.headers, json=data).json()
        msg = f'\n-----------------------------------\n'
        msg += f'✅领养物: {self.adoptingName}\n'
        msg += f'✅当前等级：{response["data"]["feedUserGameNew"]["level"]}\n'
        msg += f'✅喂养进度：{response["data"]["feedUserGameNew"]["nowScore"]}/{response["data"]["feedUserGameNew"]["needScore"]}\n'

        self.msg += msg
        print(msg)

    def feed(self):
        msg = '✅开始喂养......\n'
        url = 'https://api.shmaas.net/cap/base/credits/v2/feedUserGame'
        data = {
            'language': 'zh-cn',
            'gameId': self.adoptingId
        }
        response = requests.post(url, headers=self.headers, json=data).json()
        msg = f'-----------------------------------\n'
        if response['errCode'] == 0:
            msg += f'✅喂养成功，更新等级进度：{response["data"]["feedUserGameNew"]["nowScore"]}/{response["data"]["feedUserGameNew"]["needScore"]}\n'
        elif response['errCode'] == -2763250:
            msg += f'✅今天已经喂养过了，明天再来吧!\n'
        else:
            msg += f'❌喂养失败，{response["errMsg"]}\n'

        self.msg += msg
        print(msg)

    def query_address(self):
        msg = ''
        url = 'https://dualstack-restios.amap.com/v5/place/text'
        data = {
            'location': '121.306507,31.136091',
            'page_num': '1',
            'region': '上海市',
            'output': 'json',
            'keywords': '闵浦新苑二村',
            'city_limit': 'false',
            'sortrule': 'weight',
            'language': 'zh',
            'key': 'c358c360816bf9feebd70e46b52f3937',
            'show_fields': 'children,business,indoor,navi,photos',
            'page_size': '15',
            'scode': '55c5e446c409007de1e89b8c84342db0',
            'ts': '1715663958518'
        }
        requests.post(url, headers=self.gpsHeaders, data=data)

    def finish_query_address(self):
        json_data = {
            'language': 'zh-cn',
            'behaviorType': 10,
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/reportUserBehavior'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        if response['errCode'] == 0:
            msg = f'✅联程规划完成，兜豆：+{response["data"]["rewardValue"]}\n'
        else:
            msg = f'❌联程规划未完成，{response["errMsg"]}\n'

        self.msg += msg
        print(msg)

    def sign(self):
        json_data = {
            'uid': self.uid,
            'activityId': '55ShoppingFestival',
            'taskType': 1,
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/completeActivityTask'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        if response['errCode'] == 0:
            msg = f'✅签到成功，抽奖次数：+1\n'
        else:
            msg = f'😄{response["errMsg"]}\n'
        self.msg += msg
        print(msg)

    # 抽奖
    def lottery(self):
        url = 'https://api.shmaas.net/actbizgtw/v1/openActivityUserLuckBag'
        data = f'{{"uid":"{self.uid}","activityId":"55ShoppingFestival"}}'
        response = requests.post(url, headers=self.headers, data=data).json()
        msg = f'-----------------------------------\n'
        if response['errCode'] == 0:
            msg = f'✅抽奖成功，获得：{response["data"]["userLuckBagViewInfo"][0]["awardName"]}\n'
        elif response['errCode'] == -1961003:
            msg += f'❌抽奖失败，没有抽奖次数了!\n'
        else:
            msg += f'❌抽奖失败, cookie可能已失效！， {response["errMsg"]}\n'

        self.msg += msg
        print(msg)

    def query_finsh_status(self):
        json_data = {
            'language': 'zh-cn',
        }
        url = 'https://api.shmaas.net/cap/app/queryLowCarbonHome'
        response = requests.post(url, headers=self.headers, json=json_data).json()
        # 0：未完成 1：已完成
        if response['errCode'] == 0:
            for i in response['data']['userActivityMessages']:
                if "用户注册" in i["name"] or "用户实名" in i["name"] or "用户首单" in i["name"] or "打车出行" in i[
                    "name"]:
                    continue
                if i["finishStatus"] == 1:
                    self.needReceiveBean += i["rewardValue"]
        else:
            msg = f'❌获取任务列表信息失败， cookie可能失效：{response["errMsg"]}'
            print(msg)

    def game_share(self):
        json_data = {
            'sceneValue': 'game',
            'language': 'zh-cn',
            'behaviorType': 6,
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/reportUserBehavior'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['errCode'] == 0:
                msg = f'✅游戏成就分享成功, 兜豆+{response_json["data"]["rewardValue"]}\n'
            else:
                msg = f'❌分享失败，{response_json["errMsg"]}'
        else:
            msg = f'❌分享失败'

        self.msg += msg
        print(msg)

    def today_first_login(self):
        json_data = {
            'language': 'zh-cn',
            'behaviorType': 3,
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/reportUserBehavior'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['errCode'] == 0:
                msg = f'✅今日首次登录成功'
            else:
                msg = f'❌今日首次登录失败，{response_json["errMsg"]}'
        else:
            msg = f'❌今日首次登录失败'

        self.msg += msg
        print(msg)

    def xl_subway_ticket_list(self):
        msg = f'---------- 🐹限量抢购🐹 ----------\n'
        json_data = {
            'productIdList': [
                102,
                104,
                105,
            ],
            'sellPlatform': 'app',
        }
        url = 'https://api.shmaas.net/cap/product/queryProductInfoList'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['errCode'] == 0:
            for i in response['data']['productInfoList']:
                if i["sellOut"] == 1:
                    status = "已售罄"
                elif i["sellOut"] == 2:
                    status = "可兑换"
                else:
                    status = "其他状态"
                msg += f'🐹{i["productName"]} | {i["price"]}兜豆 | {status}\n'
        else:
            msg = f'❌获取地铁券失败，{response["errMsg"]}'

        self.msg += msg
        print(msg)

    def my_subway_tickets(self):
        msg = f'---------- 🐹可用地铁券🐹 ----------\n'
        json_data = {
            'userId': self.uid,
            'carService': 'PUB-TRAFFIC',
        }
        url = 'https://api.shmaas.net/cap/base/coupon/queryAvailableCouponCardList'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['errCode'] == 0:
            if 'records' in response['data']:
                for i in response['data']['records']:
                    msg += f'🐹【{i["title"]}】：数量{i["couponCount"]}，有效期至：{i["endTime"]}\n'
            else:
                msg += f'暂无可用地铁券'

        else:
            msg += f'❌获取地铁券失败，{response["errMsg"]}'

        self.msg += msg
        print(msg)

    def query_mall(self):
        json_data = {
            'sourceId': 'activityPlay66e9b9acf94d0293',
            'taskId': 11,
            'browseAddress': '',
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/report/browse'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['errCode'] == 0:
                msg = f'✅浏览成功\n'
            else:
                msg = f'❌浏览失败，{response_json["errMsg"]}\n'
        else:
            msg = f'❌浏览失败\n'

        self.msg += msg
        print(msg)

    def ssx_sign(self):
        json_data = {
            'sourceId': 'activityPlay66e9b9acf94d0293',
            'taskId': 10,
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/report/sign'
        response = requests.post(url, headers=self.headers, json=json_data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['errCode'] == 0 or response_json['errCode'] == -196502:
                msg = f'✅签到成功'
            else:
                msg = f'❌签到失败，{response_json["errMsg"]}'
        else:
            msg = f'❌签到失败'

        self.msg += msg
        print(msg)

    def main(self):
        title = "随申行"

        self.getUserInfo()
        self.task_list()

        self.today_first_login()
        time.sleep(random.randint(7, 15))

        self.user_game_list()
        self.get_game_info()
        time.sleep(random.randint(7, 15))

        self.feed()
        time.sleep(random.randint(10, 20))

        self.query_address()
        self.finish_query_address()
        time.sleep(random.randint(5, 10))

        self.game_share()
        time.sleep(random.randint(5, 15))

        self.ssx_sign()
        time.sleep(random.randint(5, 10))

        # self.query_mall()
        # time.sleep(random.randint(15, 20))

        self.receive()
        self.task_list()
        time.sleep(random.randint(5, 10))

        self.xl_subway_ticket_list()
        time.sleep(random.randint(5, 10))

        # 可用地铁券列表
        self.my_subway_tickets()
        time.sleep(random.randint(5, 10))

        # 通知
        # send(title, self.msg)


if __name__ == '__main__':
    env_name = 'SSX_COOKIE'
    cookie = os.getenv(env_name)
    if not cookie:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    SSX(cookie).main()
