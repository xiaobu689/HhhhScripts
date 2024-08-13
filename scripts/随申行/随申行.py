"""
随申行

路径：随申行APP
用途：签到、做任务、养宠物攒兜豆，兑换上海地铁优惠券
变量名：SSX_COOKIE
格式： 任意请求头抓 Authorization 值

---------------------------------
20240529 新增当日首次登陆、游戏成就分享
20240610 新增每日签到、浏览商场任务
20240717 增加自动领养宠物
20240808 增加浏览兜豆商城任务
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

    def receive_all_credit(self):
        headers = {
            'Host': 'r.shmaas.net',
            'X-Saic-AppId': 'maas_car',
            'Accept': 'application/json',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiJDYjE4NDM3ZGM3ZjZiNDVjMTgxOWMyNWQ5OGJmOGE0ZmMiLCJkZXZpY2VJZCI6Ikd6Y3Rabjg0NTBNU0hQODVQQk1mbnBNWXRiUlJBVGZNIiwiZXhwaXJlSW4iOjMxMjc2MzI3NTc4OTYyMiwiY3JlYXRlVGltZSI6MTcyMzI3NTc4OTYyMiwicGxhdGZvcm1Db2RlIjoiaDUiLCJhcHBJZCI6Im1hYXNfY2FyIiwiY2hhbm5lbENvZGUiOiJtYWFzIiwiYWNjb3VudE5hbWUiOiJBVVRIX0g1X1RJQ0tFVF9mNWIzOTIxODhiZmI0NzkxYmMwMGY5YjE0NmUwZGViMyIsImFjY291bnRUeXBlIjoiMTUiLCJwcm9kdWN0SWQiOjAsImVrIjoiIiwidWlkVHlwZSI6MSwidGFnIjoyfQ.m2yTPummQ7N4MT4lbFN6MLDyEtdFtMXmvUlUc5BXInBP1tHetgsmsFV_sjilHqF9md7kGecHTAYaNklP2ozLvwJNpjVmrtvQsNwhqpJ_RCwfsnbCg7dOIw2bnW5EWHCPh5_kr5B7ttf15bftwwHJt3E6NnCcHSTjeZqEZcpRG4g',
            'X-Saic-Channel': 'maas',
            'Sec-Fetch-Site': 'cross-site',
            'X-Saic-Device-Id': 'GzctZn8450MSHP85PBMfnpMYtbRRATfM',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json',
            'Origin': 'https://www.shmaas.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 x-isapp=1&bundleId=cn.shmaas.maas',
            'Referer': 'https://www.shmaas.cn/',
            'Connection': 'keep-alive',
            'X-Saic-Platform': 'h5',
            'Sec-Fetch-Dest': 'empty',
        }

        json_data = [
            {
                'sys': {
                    'dataId': 2908,
                    'dataDesc': '领取兜豆组件-【一键领取】按钮点击',
                    'dataExtra': '{"componentId":"receivepoint_cbc65687"}',
                    'tag': '',
                    'userid': 'Cb18437dc7f6b45c1819c25d98bf8a4fc',
                    'channel': '',
                    'sourceId': '',
                    'osName': 'ios',
                    'isapp': True,
                    'deviceId': 'GzctZn8450MSHP85PBMfnpMYtbRRATfM',
                    'timestamp': 1723275796267,
                    'newDeviceId': '633EB41D5EEC41B1BA90E94C0A37D1D6',
                    'appId': 'maas_car',
                    'url': 'https://www.shmaas.cn/magic/dist/56ddf9d392c71a3ce2e0e2c69d26e4e1/index.html?needToken=1&language=zh-cn&ticket=AUTH_H5_TICKET_f5b392188bfb4791bc00f9b146e0deb3&appid=maas_car',
                    'platform': 'h5',
                    'hostPlatform': 'app',
                    'hostPlatformKey': 'default',
                    'serverType': 'prod',
                    'cityCode': '310100',
                    'module': 'tmagic',
                },
                'cus': {},
            },
        ]
        url = 'https://r.shmaas.net/receive/samplingreceiver/receivedata'
        response_json = requests.post(url, headers=headers, json=json_data).json()
        if response_json['errCode'] == 0:
            print(f'✅领取兜豆成功！')
        else:
            print(f'❌领取兜豆失败|{response_json["errMsg"]}')


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


    def user_game_list(self):
        gameName = ''
        json_data = {
            'language': 'zh-cn',
        }
        url = 'https://api.shmaas.net/cap/base/credits/v2/queryUserGameList'
        response = make_request(url, json_data=json_data, method='post', headers=self.headers)
        if response and response['errCode'] == 0:
            for i in response['data']['gameCardInfo']:
                if i["type"] == 2:  # type 2喂养中
                    self.adoptingId = i["gameId"]
                    if i["gameId"] == '998':
                        gameName = '和平鸽'
                    elif i["gameId"] == '999':
                        gameName = '白玉兰'
                    self.adoptingName = gameName
                    break

    def get_game_info(self):
        msg = ''
        url = 'https://api.shmaas.net/cap/base/credits/queryNowAdoptInfo'
        data = {"language": "zh-cn"}
        response = requests.post(url, headers=self.headers, json=data).json()
        msg += f'✅领养物: {self.adoptingName}\n'
        msg += f'✅当前等级：{response["data"]["feedUserGameNew"]["level"]}\n'
        msg += f'✅喂养进度：{response["data"]["feedUserGameNew"]["nowScore"]}/{response["data"]["feedUserGameNew"]["needScore"]}\n'

        self.msg += msg
        print(msg)

    # 领养宠物
    def adopt(self):
        gameIds = ['998', '999']
        gameName = ''
        gameId = random.choice(gameIds)
        if gameId == '998':
            gameName = '和平鸽'
        elif gameId == '999':
            gameName = '白玉兰'
        json_data = {
            'language': 'zh-cn',
            'gameId': gameId,
        }
        url = 'https://api.shmaas.net/cap/base/credits/v2/adoptUserGame'
        response = requests.post(url, headers=self.headers, json=json_data)
        response_json = response.json()
        if response_json['errCode'] == 0:
            msg = f'✅领养成功！| 拿下: {gameName}'
            print(msg)
        else:
            msg = f'❌领养失败，{response_json["errMsg"]}'
            print(msg)

    def feed(self):
        msg = '✅开始喂养......\n'
        url = 'https://api.shmaas.net/cap/base/credits/v2/feedUserGame'
        data = {
            'language': 'zh-cn',
            'gameId': self.adoptingId
        }
        response = requests.post(url, headers=self.headers, json=data).json()
        now_score = response["data"]["feedUserGameNew"]["nowScore"]
        need_score = response["data"]["feedUserGameNew"]["needScore"]
        msg = f'-----------------------------------\n'
        if response['errCode'] == 0:
            msg += f'✅喂养成功，更新等级进度：{now_score-10}/{need_score}➡️{now_score}/{need_score}\n'
            if now_score == 100:
                print("✅喂养完成，开始领养新的宠物")
                self.adopt()
        elif response['errCode'] == -2763250:
            msg += f'✅今天已经喂养过了，明天再来吧!\n'
        else:
            msg += f'❌喂养失败，{response["errMsg"]}\n'

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
                msg = f'✅登录成功'
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

    def view_mall(self):
        json_data = {
            'sourceId': 'activityPlay66e9b9acf94d0293',
            'taskId': 57,
            'browseAddress': '',
        }
        url = 'https://api.shmaas.net/actbizgtw/v1/report/browse'
        response_json = requests.post(url, headers=self.headers, json=json_data).json()
        if response_json['errCode'] == 0:
            print(f'✅浏览兜豆商城成功')
        else:
            print(f'❌浏览兜豆商城失败，{response_json["errMsg"]}')

    def main(self):
        title = "随申行"
        self.getUserInfo()

        self.today_first_login()
        time.sleep(random.randint(7, 15))

        self.ssx_sign()
        time.sleep(random.randint(5, 10))

        self.user_game_list()
        self.get_game_info()
        time.sleep(random.randint(7, 15))
        self.feed()
        time.sleep(random.randint(5, 10))

        self.view_mall()
        time.sleep(random.randint(5, 10))

        # self.receive()
        self.receive_all_credit()
        time.sleep(random.randint(5, 10))

        # self.xl_subway_ticket_list()
        # time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    env_name = 'SSX_COOKIE'
    cookie = os.getenv(env_name)
    if not cookie:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    SSX(cookie).main()
