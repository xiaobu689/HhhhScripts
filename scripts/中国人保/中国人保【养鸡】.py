"""
中国人保-养鸡

变量名: ZGRBYJ
cron: 35 7,23 * * *
const $ = new Env("中国人保-养鸡");
"""
import os
import random
import time
from datetime import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import save_result_to_file
from sendNotify import send
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class RUN():
    name = "中国人保-养鸡"

    def __init__(self, user_id):
        UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PBrowser/3.16.0 PiccApp/6.22.6 &&webViewInfo=3.16.0&&appInfo=piccApp&&appVersion=6.22.6'
        self.user_id = user_id
        self.access_token = ''
        self.mToken = ''
        self.mHeaders = {
            'Host': 'm.picclife.cn',
            'Authorization': self.mToken,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': UA,
        }

    # ============================================= 云养小鸡 =============================================#
    def chicken_login(self):
        params = {
            'userId': self.user_id,
        }
        try:
            response = requests.get('https://m.picclife.cn/chicken-api/h5login', params=params, headers=self.mHeaders)
            if not response or response.status_code != 200:
                print('鸡场登录异常')
                save_result_to_file("error", self.name)
                return False
            response_json = response.json()
            self.access_token = response_json["access_token"]
            token = f'bearer{response_json["access_token"]}'
            refresh_token = response_json["refresh_token"]
            self.mToken = token
            self.mHeaders['Authorization'] = token
            save_result_to_file("success", self.name)
            print(f"🐔鸡场登录成功")
            return True
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            save_result_to_file("error", self.name)
            return False

    # 领取所有饲料
    def chicken_collect_tall(self):
        response = requests.post('https://m.picclife.cn/chicken-api/p/chicken/tashcollectall',
                                     headers=self.mHeaders)
        print(response.text)
        response_json = response.json()
        if response_json['code'] == 200:
            print(f'🐔✅领取全部饲料成功')
        else:
            print(f'🐔❌领取全部饲料失败 | {response_json["message"]}')

    # 收鸡蛋
    def chicken_collect_egg(self):
        response_json = requests.post('https://m.picclife.cn/chicken-api/p/chicken/collectegg',
                                     headers=self.mHeaders).json()
        if response_json['code'] == 200:
            print(f'🐔{response_json["data"]["name"]} | ✅收鸡蛋成功')
        else:
            print(f'🐔{response_json["data"]["name"]} | ❌收鸡蛋失败 | {response_json["message"]}')

    def chicken_get_taskId(self, tashId):
        response_json = requests.get('https://m.picclife.cn/chicken-api/p/chicken/listtask',
                                     headers=self.mHeaders).json()
        if response_json['code'] == 200:
            tasks_list = response_json['result']['dailyTasksList']
            for item in tasks_list:
                taskId = item["taskId"]
                if item["taskSort"] == tashId:
                    task_id = int(taskId)
                    return task_id

            return None


    # 鸡场每日任务列表
    def chicken_daily_task(self):
        response = requests.get('https://m.picclife.cn/chicken-api/p/chicken/listtask', headers=self.mHeaders)
        response_json = response.json()
        if response_json['code'] == 200:
            list = response_json['result']['dailyTasksList']
            for item in list:
                if "邀请" in item['taskName']:
                    continue
                taskStatus = item['taskStatus']
                taskSort = item['taskSort']
                if taskStatus == 0:
                    # 阅读健康资讯
                    if item["taskSort"] == 34:
                        print(f'开始阅读健康资讯......')
                        for i in range(3):
                            self.view_news_task(taskSort)
                            time.sleep(5)
                            self.do_task_collect(taskSort)
                            time.sleep(5)
                    # 浏览保险产品【废的else分支】
                    elif item["taskSort"] == 33:
                        print(f'开始浏览保险产品......')
                        for i in range(3):
                            self.view_insurance_task()
                            time.sleep(16)
                    # 分享朋友圈
                    elif item["taskSort"] == 112 and taskStatus == 0:
                        self.do_share_task()
                        time.sleep(5)
                        self.do_task_collect(taskSort)
                    # 进入庄园
                    # elif item["taskSort"] == 35:
                    #     self.do_share_task()
                    #     time.sleep(5)
                    #     self.do_task_collect(taskSort)
                    # 使用道具
                    elif item["taskSort"] == 113:
                        print()
                    # 抽奖
                    elif item["taskSort"] == 111:
                        print()
                    # 福寿年年
                    elif item["taskSort"] == 110:
                        print()
                    # 召回好友
                    elif item["taskSort"] == 32:
                        print()



    def do_share_task(self):
        json_data = {
            'activityCode': '2',
            'shareType': '分享朋友圈',
        }
        response = requests.post('https://m.picclife.cn/chicken-api/p/chicken/addShareRecord', headers=self.mHeaders, json=json_data)
        response_json = response.json()
        if response_json['code'] == 200:
            print(f'✅分享朋友圈成功')
        else:
            print(f'❌分享朋友圈失败')

    # 连续签到[早5:00-9:00打卡得翻倍奖励]
    def daily_sign(self):
        # 普通签到，非【5-9】
        params = {
            'clockNumber': '1',
            'foodQuantity': '0',
        }
        # 非【5-9】连签3天，得2份
        # params = {
        #     'clockNumber': '2',
        #     'foodQuantity': '0',
        # }
        # 普通签到【5-9】时间内签到
        # params = {
        #     'clockNumber': '？？？',
        #     'foodQuantity': '0',
        # }
        url = 'https://m.picclife.cn/chicken-api/p/chicken/tashdailyfinish'
        response = requests.get(url, params=params, headers=self.mHeaders)

    # 浏览保险产品
    def view_insurance_task(self):
        json_data = {
            'access_token': self.access_token,
            'activity_code': '100026',
            'random_num': '78001861E13',
            'timestamp': 1720670658778,
            'sign': 'f5792d268d6c4b66b3b4e61d39bda284b3d0cdd9',
            'platform': 7,
            'mission_code': '33',
        }
        response = requests.post('https://m.picclife.cn/ebs-api/wap/api/order/chicken-run/mission', headers=self.mHeaders, json=json_data)
        print(response.text)
        response_json = response.json()
        if response_json["success"]:
            print(f'🐔浏览保险产品成功')
        else:
            print(f'❌浏览保险产品失败')

    # 阅读健康资讯
    def view_news_task(self, taskSort):
        params = {
            'tashId': taskSort,
        }
        response_json = requests.post('https://m.picclife.cn/chicken-api/p/chicken/tashfinish', params=params, headers=self.mHeaders).json()
        if response_json["code"] == 200:
            print(f'🐔任务完成')
        else:
            print(f'❌任务失败')

    def do_task_collect(self, taskSort):
        task_id = self.chicken_get_taskId(taskSort)
        if task_id is not None:
            params = {
                'tashId': task_id,
            }
            response_json = requests.post('https://m.picclife.cn/chicken-api/p/chicken/tashcollect', params=params, headers=self.mHeaders).json()
            print("response2_json=", response_json)
            if response_json["code"] == 200:
                print(f'🐔收饲料成功')
            else:
                print(f'❌收饲料失败')

    # 喂鸡
    def feed_chicken(self):
        params = {
            'foodQuantity': '180',
        }
        response = requests.post('https://m.picclife.cn/chicken-api/p/chicken/addfeedfood_v3', params=params, headers=self.mHeaders)
        print("response3=", response.text)
        response_json = response.json()
        if response_json["code"] == 200:
            print(f'🐔喂鸡成功')
            feedfoodQuantity = response_json["result"]["feedfoodQuantity"]
            foodHour = response_json["result"]["foodHour"]
            foodCount = response_json["result"]["foodCount"]
            leftfood = response_json["result"]["leftfood"]
            print(f'🐔剩余可用饲料: {foodCount} | 鸡盆剩余饲料：{leftfood} | 预计{foodHour}吃完')
        else:
            print(f'❌喂鸡失败 | {response_json["message"]}')

    def get_egg_growth(self):
        response = requests.get('https://m.picclife.cn/chicken-api/p/chicken/feedfodderfood_v3', headers=self.mHeaders)
        response_json = response.json()
        if response_json["code"] == 200:
            chickfoodStatus = response_json["result"]["chickfoodStatus"]
            if chickfoodStatus == "0":
                status = '快饿死了'
            elif chickfoodStatus == "1":
                status = '干饭中'
            eggPer = response_json["result"]["eggPer"]
            foodCount = response_json["result"]["foodCount"]
            print(f'🐔鸡蛋成长值: {eggPer}/100 | 🐔鸡在干嘛: {status}')
            return eggPer, foodCount, chickfoodStatus
        else:
            print(f'❌鸡蛋成长值失败 | {response_json["message"]}')
            return None, None, None

    def my_egg_list(self):
        response = requests.get('https://m.picclife.cn/chicken-api/p/chicken/listegg', headers=self.mHeaders)
        response_json = response.json()
        if response_json["code"] == 200:
            eggList = response_json["result"]["list"]
            if len(eggList) > 0:
                return len(eggList)
        else:
            return 0

    def chicken_sell_egg(self):
        collectTime = datetime.now().strftime('%Y.%m.%d')
        params = {
            'eggStatus': '3',
            'collectTime': collectTime,
        }
        response = requests.post('https://m.picclife.cn/chicken-api/p/chicken/eggSell', params=params, headers=self.mHeaders)
        response_json = response.json()
        if response_json["code"] == 200:
            print(f'🐔卖鸡蛋成功')
        else:
            print(f'❌卖鸡蛋失败')

    def chicken_user_info(self):
        response = requests.get('https://m.picclife.cn/chicken-api/p/chicken/userinfo', headers=self.mHeaders)
        response_json = response.json()
        if response_json["code"] == 200:
            userName = response_json["result"]["userName"]
            coinCount = response_json["result"]["coinCount"]
            msg = f'🐔主人: {userName} | 金币: {coinCount}个'
            print(msg)
            if coinCount >= 600:
                send("中国人保养鸡金币达标通知", msg)
            return True
        else:
            print(f'❌鸡信息失败')
            return False

    def main(self):
        print(f"\n======== ▷ 云养小鸡 ◁ ========")
        if self.chicken_login():
            # 先把饲料领一遍
            self.chicken_collect_tall()
            time.sleep(random.randint(10, 15))

            # 做每日任务领饲料
            self.chicken_daily_task()
            time.sleep(random.randint(10, 15))

            # 喂鸡
            eggPer, foodCount, chickfoodStatus = self.get_egg_growth()
            if eggPer is not None and foodCount is not None and chickfoodStatus is not None:
                if eggPer == 100:
                    # 捡鸡蛋
                    self.chicken_collect_egg()
                else:
                    # 喂鸡
                    print(f'🐔捡鸡蛋捡个屁 | 还没下蛋呢， 进度: {eggPer}/100')
                    if chickfoodStatus == '0' and foodCount >= 180:
                        self.feed_chicken()
                        time.sleep(random.randint(10, 15))
                    elif foodCount < 180:
                        print(f'🐔喂鸡失败, 饲料不足 | 剩余饲料: {foodCount}g/需要饲料: 180g')
            time.sleep(random.randint(10, 15))

            # 卖鸡蛋
            eggs = self.my_egg_list()
            if eggs > 0:
                self.chicken_sell_egg()
            else:
                print(f'❌卖鸡蛋失败 | 还没收鸡蛋呢')
            time.sleep(random.randint(5, 10))

            # 再最后领一遍饲料
            self.chicken_collect_tall()
            time.sleep(random.randint(5, 10))

            # 信息汇总
            self.chicken_user_info()


if __name__ == '__main__':
    env_name = 'ZGRBYJ'
    user_id = os.getenv(env_name)
    user_id = 'b7617974424ef68e693237b27fd2e244'
    if not user_id:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    RUN(user_id).main()
