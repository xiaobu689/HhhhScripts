"""
招商信诺

软件：招商信诺APP
抓包：微信登陆绑定手机，抓微信小程序招商信诺服务中心的包【https://member.cignacmb.com/mini/member/interface/login】
#青龙填写变量zsxn，值为unionid@miniopenid@mobile，多个账号就创建多个变量
变量名: ZSXN
变量值：unionid#miniopenid#mobile
多账号&连接

cron: 0 0,8 * * *
const $ = new Env("招商信诺");

--------------------------
20240714 修复CK有效期短问题
20240804 增加等级宝箱抽奖、转盘抽奖
20250805 增加猜硬币
--------------------------
"""
import base64
# print("维护中")
# exit(0)
import json
import os
import random
import re
import time
import requests
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import save_result_to_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class ZSXN():
    name = "招商信诺"

    def __init__(self, token):
        unionid, miniopenid, mobile = token.split('#')
        self.token = ''
        self.unionid = unionid
        self.miniopenid = miniopenid
        self.mobile = mobile
        self.lottery_count = 0
        self.guess_coin_count = 0
        self.total_score = 0
        self.headers = {
            'authority': 'vip.ixiliu.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'access-token': '',
            'content-type': 'application/json;charset=utf-8',
            'platform': 'MP-WEIXIN',
            'referer': 'https://servicewechat.com/wx9a2dc52c95994011/91/page-frame.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sid': '10009',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
            'xweb_xhr': '1',
        }

    def user_login(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'requestChannel': 'MINI',
            'Authorization': 'Bearer_',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a32) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wxfdbf8b13d7468707/206/page-frame.html',
        }
        payload = {
            "unionid": self.unionid,
            "miniOpenId": self.miniopenid,
            "mobile": self.mobile,
            "miniOpenid": self.miniopenid,
            "sensorDeviceId": self.miniopenid
        }
        data = {'param': json.dumps(payload)}
        response = requests.post('https://member.cignacmb.com/mini/member/interface/login', headers=headers, data=data)
        if not response or response.status_code != 200:
            print(f"❌登陆失败 | {response.text}")
            save_result_to_file("error", self.name)
            return False
        response_json = response.json()
        if response_json["respCode"] == "00":
            print("✅登录成功")
            token = response.headers.get('token', '')
            self.headers['access-token'] = f'Bearer_{token}'
            self.token = f'Bearer_{token}'
            save_result_to_file("success", self.name)
            return True
        else:
            print(f"❌登陆失败 | {response_json['respDesc']}")
            save_result_to_file("error", self.name)
            return False

    def user_info(self):
        response = requests.get('https://vip.ixiliu.cn/mp/user/info', headers=self.headers)
        if not response or response.status_code != 200:
            print("获取用户信息失败")
            return
        response_json = response.json()
        if response_json['code'] == 0:
            print(
                f'🐶{response_json["data"]["userInfo"]["mobile"]} | 💰{response_json["data"]["userInfo"]["points_total"]}积分\n')

    def init_lottery(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/index.html?appVersion=5.24.10',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }
        data = {
            'param': 'e30=',
        }
        url = 'https://member.cignacmb.com/shop/member/interface/initPointsDraw'
        response = requests.post(url, headers=headers, data=data)
        if not response or response.status_code != 200:
            print("抽奖基础信息异常：", response.text)
            return
        response_json = response.json()
        if response_json['respCode'] == '00':
            lottery_count = response_json['respData']['lotteryCount']
            self.lottery_count = lottery_count
            print(f'🐱现有积分: {response_json["respData"]["integral"]} | 🐶今日剩余可抽奖次数: {lottery_count}')
        else:
            print(f'❌抽奖失败基础信息获取失败：{response_json["respDesc"]}')

    def do_lottery(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/index.html?appVersion=5.24.10',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

        data = {
            'param': 'e30=',
        }

        response = requests.post(
            'https://member.cignacmb.com/shop/member/interface/doPointsDraw',
            headers=headers,
            data=data,
        )
        if not response or response.status_code != 200:
            print("抽奖异常：", response.text)
            return
        response_json = response.json()
        if response_json['respCode'] == '00':
            print(f'✅抽奖成功 | 抽奖结果: {response_json["respData"]["prizeName"]}')
        else:
            print(f'❌抽奖失败：{response_json["respDesc"]}')

    def points_info(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/?appVersion=5.24.10',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

        data = {
            'param': 'e30=',
        }

        response = requests.post(
            'https://member.cignacmb.com/shop/member/interface/queryScoreStatisticsMonth',
            headers=headers,
            data=data,
        )

        if not response or response.status_code != 200:
            print('获取积分信息失败')
            return
        response_json = response.json()
        if response_json['respCode'] == '00':
            self.total_score = response_json['respData']['totalScore']
            print(
                f'💰总积分: {response_json["respData"]["totalScore"]}')
        else:
            print(f'获取积分信息失败: {response_json["respDesc"]}')

    # def user_info(self):

    def user_task_list(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Authorization': self.token,
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

        response = requests.get('https://hms.cignacmb.com/activity/cignaInvestment/getUserTaskList',
                                headers=headers)
        if not response or response.status_code != 200:
            print('获取任务列表失败')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            list = response_json['data']['allTask']
            return list
        else:
            return None

    def get_task_recordId(self, taskCode):
        recordId = 0
        list = self.user_task_list()
        for task in list:
            if task['taskCode'] == taskCode:
                recordId = task['recordId']
                break
        return recordId

    def do_candy_task(self):
        list = self.user_task_list()
        if list is None:
            return
        for task in list:
            # 如果实名认证和完善资料则跳过
            if task['taskName'] == '实名认证' or task['taskName'] == '完善个人信息':
                continue
            # 执行任务
            # -1|待完成， 1|已完成 0|待领取
            if task['status'] == 1:
                continue
            self.update_task_status(task["taskCode"], task['taskName'])
            time.sleep(random.randint(15, 20))
            recordId = self.get_task_recordId(task["taskCode"])
            if recordId != 0:
                self.receive_candy(recordId)

    def update_task_status(self, taskCode, taskName):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://hms.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

        data = {
            'taskCode': taskCode,
        }

        response = requests.post(
            'https://hms.cignacmb.com/activity/cignaInvestmentTask/updateTaskStatus', headers=headers,
            data=data)
        if not response or response.status_code != 200:
            print('更新任务状态异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print(f'✅{taskName} | 状态更新成功')
        else:
            print('❌更新任务状态失败')

    def receive_candy(self, recordId):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://hms.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

        data = {
            'recordId': recordId,
        }

        response = requests.post(
            'https://hms.cignacmb.com/activity/cignaInvestment/receiveCandy', headers=headers, data=data)
        if not response or response.status_code != 200:
            print('领取糖果异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print(f'✅领取糖果成功 | 糖果+{response_json["data"][0]["disposableCandyNum"]}')
        else:
            print('❌领取糖果失败，', response_json['msg'])

    def invest_candy(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Authorization': self.token,
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://hms.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }

        response = requests.post('https://hms.cignacmb.com/activity/cignaInvestment/investCandy',
                                 headers=headers)
        if not response or response.status_code != 200:
            print('领取糖果异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print("✅成功投喂糖果")
        else:
            print("❌投喂糖果失败，", response_json['msg'])

    def init_user_info(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Authorization': self.token,
            'userId': '7181805',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://hms.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }
        url = 'https://hms.cignacmb.com/activity/cignaInvestment/initializeUserInfo'
        response = requests.post(url, headers=headers)
        if not response or response.status_code != 200:
            print('获取用户信息异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            candy_num = response_json['data']['candyNum']
            growth_level = response_json['data']['growthLevel']
            growth_level_candy_num = response_json['data']['growthLevelCandyNum']
            received_naomi_num = response_json['data']['receivedNaomiNum']  # 27%
            print(f'✅当前进度: {received_naomi_num}')
            print(f"✅用户信息获取成功 | 等级：{growth_level} | 糖果：{candy_num} | 等级成长值：{growth_level_candy_num}")
        else:
            print("❌获取用户信息失败，", response_json['msg'])

    # 健康任务
    def healthy_task(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'userId': '7181805',
            'Referer': 'https://hms.cignacmb.com/wmpages/app-rest/module/healthfile/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M&isNewHealthRecords=Y',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'X-Request-Platform': 'web',
            'X-Device-Id': '123456',
            'Origin': 'https://hms.cignacmb.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            'X-Request-Version': '5.24.10',
            'Connection': 'keep-alive',
            'Authorization': self.token,
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Sec-Fetch-Mode': 'cors',
        }
        data = {
            'lastTaskId': '',
        }
        response = requests.post('https://hms.cignacmb.com/health/nuo/queryHealthTaskList',
                                 headers=headers, data=data)
        if not response or response.status_code != 200:
            print('获取健康任务异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            list = response_json['data']
            for task in list:
                # taskState 02|未完成 03|已完成
                if task["taskState"] == '02':
                    taskId = task['id']
                    taskName = task['taskName']
                    taskType = task['taskType']
                    receiveAward = task['awardNum']
                    taskCode = task['taskCode']
                    self.do_health_task(taskId, taskType, receiveAward, taskCode, taskName)
                    time.sleep(random.randint(15, 20))
                    self.receive_helth_task(taskId, taskType)

        else:
            print("❌获取健康任务失败，", response_json['msg'])

    def do_health_task(self, taskId, taskType, receiveAward, taskCode, taskName):
        headers = {
            'Host': 'hms.cignacmb.com',
            'userId': '7181805',
            'Referer': 'https://hms.cignacmb.com/wmpages/app-rest/module/healthfile/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M&isNewHealthRecords=Y',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'X-Request-Platform': 'web',
            'X-Device-Id': '163CBC75-91C1-4DC0-8EA4-C3286B29C51E',
            'Origin': 'https://hms.cignacmb.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            'X-Request-Version': '5.24.10',
            'Connection': 'keep-alive',
            'Authorization': self.token,
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
        }
        data = {
            'taskId': taskId,
            'taskType': taskType,
            'receiveAward': receiveAward,
            'taskCode': taskCode,
        }
        response = requests.post('https://hms.cignacmb.com/health/nuo/toComplete', headers=headers,
                                 data=data)
        if not response or response.status_code != 200:
            print('获取健康任务异常')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print(f"✅任务完成 | {taskName}")
        else:
            print("❌任务完成失败", response_json['msg'])

    def receive_helth_task(self, id, taskType):
        headers = {
            'Host': 'hms.cignacmb.com',
            'userId': '7181805',
            'Referer': 'https://hms.cignacmb.com/wmpages/app-rest/module/healthfile/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M&isNewHealthRecords=Y',
            # 'Cookie': 'GPHMS=SV-HMS-80-02; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221903a207d171d0c-00cc4ef12e489f-2702704-329160-1903a207d18251a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwM2EyMDdkMTcxZDBjLTAwY2M0ZWYxMmU0ODlmLTI3MDI3MDQtMzI5MTYwLTE5MDNhMjA3ZDE4MjUxYSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221903a207d171d0c-00cc4ef12e489f-2702704-329160-1903a207d18251a%22%7D; sajssdk_2015_cross_new_user=1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjA2MDY1QjhFMzNEMDg0MzRBNkZGQ0E2MTE5RENBNUJBODIxMTcxIiwibG9naW5UaW1lIjoiMTcxODg3NzgxMTk2OCIsIm5iZiI6MTcxODg3NzgxMSwiZXhwdCI6MTcxODk2NDIxMTk2OCwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMDA4NzQxMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcxODg3NzgxMX0.ZpbJfVcqx3AlDiZt99XUTpbvpSOoGCHigHfXhdeyS7M;',
            'X-Request-Platform': 'web',
            'X-Device-Id': '163CBC75-91C1-4DC0-8EA4-C3286B29C51E',
            'Origin': 'https://hms.cignacmb.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            # 'Content-Length': '15',
            'X-Request-Version': '5.24.10',
            'Connection': 'keep-alive',
            'Authorization': self.token,
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
        }
        data = {
            'id': id,
            'taskType': taskType,
        }
        response = requests.post('https://hms.cignacmb.com/health/nuo/claimYourReward',
                                 headers=headers, data=data)
        if not response or response.status_code != 200:
            print('领取失败')
            return
        response_json = response.json()
        if response_json['statusCode'] == '0':
            print('✅健康任务奖励领取成功')
        else:
            print('❌健康任务奖励领取失败, ', response_json['msg'])

    # 等级宝箱抽奖
    def user_treasure_box(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'userId': '8017656',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjE2Rjg3NUVBM0RBNUQwMUMwRUEyN0NDNzA3NjU5REVEMzgwMTMwIiwibG9naW5UaW1lIjoiMTcyMjc2NTI5MTM4NSIsIm5iZiI6MTcyMjc2NTI5MSwiZXhwdCI6MTcyMjg1MTY5MTM4NSwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMzk3NDg5MSwidXNlcklkIjoiODAxNzY1NiIsImlhdCI6MTcyMjc2NTI5MX0.znlxOp7PAObnlIsQ3DlHiH10r-zven_TkBEOerHl_j8;',
            'Authorization': 'Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjE2Rjg3NUVBM0RBNUQwMUMwRUEyN0NDNzA3NjU5REVEMzgwMTMwIiwibG9naW5UaW1lIjoiMTcyMjc2NTI5MTM4NSIsIm5iZiI6MTcyMjc2NTI5MSwiZXhwdCI6MTcyMjg1MTY5MTM4NSwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMzk3NDg5MSwidXNlcklkIjoiODAxNzY1NiIsImlhdCI6MTcyMjc2NTI5MX0.znlxOp7PAObnlIsQ3DlHiH10r-zven_TkBEOerHl_j8',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjE2Rjg3NUVBM0RBNUQwMUMwRUEyN0NDNzA3NjU5REVEMzgwMTMwIiwibG9naW5UaW1lIjoiMTcyMjc2NTI5MTM4NSIsIm5iZiI6MTcyMjc2NTI5MSwiZXhwdCI6MTcyMjg1MTY5MTM4NSwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMzk3NDg5MSwidXNlcklkIjoiODAxNzY1NiIsImlhdCI6MTcyMjc2NTI5MX0.znlxOp7PAObnlIsQ3DlHiH10r-zven_TkBEOerHl_j8',
            'Accept-Language': 'zh-cn',
        }
        url = 'https://hms.cignacmb.com/activity/cignaInvestment/getUserTreasureBox'
        response_json = requests.get(url, headers=headers).json()
        if response_json['statusCode'] == '0':
            treasureBoxNum = response_json['data']['treasureBoxNum']
            isReceived = response_json['data']['isReceived']
            if isReceived > 0:
                self.user_treasure_box_lottery()
        else:
            print(f'❌等级宝箱信息获取异常 | {response_json["msg"]}')

    def user_treasure_box_lottery(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'userId': '8017656',
            'Accept-Language': 'zh-cn',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://hms.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.24.10;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjE2Rjg3NUVBM0RBNUQwMUMwRUEyN0NDNzA3NjU5REVEMzgwMTMwIiwibG9naW5UaW1lIjoiMTcyMjc2NTI5MTM4NSIsIm5iZiI6MTcyMjc2NTI5MSwiZXhwdCI6MTcyMjg1MTY5MTM4NSwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMzk3NDg5MSwidXNlcklkIjoiODAxNzY1NiIsImlhdCI6MTcyMjc2NTI5MX0.znlxOp7PAObnlIsQ3DlHiH10r-zven_TkBEOerHl_j8;',
            'Referer': 'https://hms.cignacmb.com/hms-act/nurturing_game_reset/index.html?appVersion=5.24.10&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjE2Rjg3NUVBM0RBNUQwMUMwRUEyN0NDNzA3NjU5REVEMzgwMTMwIiwibG9naW5UaW1lIjoiMTcyMjc2NTI5MTM4NSIsIm5iZiI6MTcyMjc2NTI5MSwiZXhwdCI6MTcyMjg1MTY5MTM4NSwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyMzk3NDg5MSwidXNlcklkIjoiODAxNzY1NiIsImlhdCI6MTcyMjc2NTI5MX0.znlxOp7PAObnlIsQ3DlHiH10r-zven_TkBEOerHl_j8',
        }

        data = {
            'treasureBoxNum': '1',
        }

        url = 'https://hms.cignacmb.com/activity/cignaInvestment/lottery'
        response_json = requests.post(url, headers=headers, data=data).json()
        if response_json['statusCode'] == '0':
            prizeName = response_json['data']['prizeName']
            print(f'✅等级宝箱抽奖成功 | 获得奖品：{prizeName}')
        else:
            print('❌等级宝箱抽奖失败, ', response_json['msg'])

    def keep_step_challenge(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Referer': 'https://hms.cignacmb.com/wmpages/app-rest/module/healthfile/index.html?appVersion=5.25.16&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjdGNURDRTMzNEU4N0FGQzZCMTIyQTdEN0U2RTlFN0E4Njc2MTE2IiwibG9naW5UaW1lIjoiMTcyMjgzNzMwMTcwMSIsIm5iZiI6MTcyMjgzNzMwMSwiZXhwdCI6MTcyMjkyMzcwMTcwMiwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyNDA0NjkwMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcyMjgzNzMwMX0.ivNa7mCgxN5TREjRhywD8jBmJWA8kyDs1TUhIrP-K6A&__t=1722840199069&isNewHealthRecords=Y',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.25.16;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjdGNURDRTMzNEU4N0FGQzZCMTIyQTdEN0U2RTlFN0E4Njc2MTE2IiwibG9naW5UaW1lIjoiMTcyMjgzNzMwMTcwMSIsIm5iZiI6MTcyMjgzNzMwMSwiZXhwdCI6MTcyMjkyMzcwMTcwMiwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyNDA0NjkwMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcyMjgzNzMwMX0.ivNa7mCgxN5TREjRhywD8jBmJWA8kyDs1TUhIrP-K6A;',
            'X-Request-Platform': 'web',
            'X-Device-Id': '163CBC75-91C1-4DC0-8EA4-C3286B29C51E',
            'Origin': 'https://hms.cignacmb.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            'X-Request-Version': '5.25.16',
            'Connection': 'keep-alive',
            'Authorization': self.token,
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
        }
        data = {
            'flag': '00',
        }
        url = 'https://hms.cignacmb.com/health/app/healthTasks/queryReceiveTaskDetails'
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        # 获取当前日期
        current_date = datetime.now().strftime("%Y/%m/%d")
        if response_json['statusCode'] == '0' and response_json["data"] is not None:
            healthTaskDrawsNumber = response_json['data']['healthTaskDrawsNumber']
            healthTaskName = response_json['data']['healthTaskName']
            healthTaskDesc = response_json['data']['healthTaskDesc']
            healthTaskDateList = response_json['data']['healthTaskDateList']
            print(f'🐶{healthTaskName} | {healthTaskDesc} | 达标得{healthTaskDrawsNumber}次抽奖机会')
            for healthTaskDate in healthTaskDateList:
                diaryDate = healthTaskDate['diaryDate']
                maxSteps = healthTaskDate['maxSteps']
                if current_date == diaryDate:
                    print(f'🐶今日步数：{maxSteps}步')
                    if maxSteps >= 8000:
                        print('✅今日已达标')
                    else:
                        print('❌今日未达标')

    def sync_user_step(self):
        headers = {
            'Host': 'hms.cignacmb.com',
            'Referer': 'https://hms.cignacmb.com/wmpages/app-rest/module/healthfile/index.html?appVersion=5.25.16&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjdGNURDRTMzNEU4N0FGQzZCMTIyQTdEN0U2RTlFN0E4Njc2MTE2IiwibG9naW5UaW1lIjoiMTcyMjgzNzMwMTcwMSIsIm5iZiI6MTcyMjgzNzMwMSwiZXhwdCI6MTcyMjkyMzcwMTcwMiwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyNDA0NjkwMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcyMjgzNzMwMX0.ivNa7mCgxN5TREjRhywD8jBmJWA8kyDs1TUhIrP-K6A&__t=1722840199069&isNewHealthRecords=Y',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.25.16;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjdGNURDRTMzNEU4N0FGQzZCMTIyQTdEN0U2RTlFN0E4Njc2MTE2IiwibG9naW5UaW1lIjoiMTcyMjgzNzMwMTcwMSIsIm5iZiI6MTcyMjgzNzMwMSwiZXhwdCI6MTcyMjkyMzcwMTcwMiwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyNDA0NjkwMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcyMjgzNzMwMX0.ivNa7mCgxN5TREjRhywD8jBmJWA8kyDs1TUhIrP-K6A;',
            'X-Request-Platform': 'web',
            'X-Device-Id': '163CBC75-91C1-4DC0-8EA4-C3286B29C51E',
            'Origin': 'https://hms.cignacmb.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            'X-Request-Version': '5.25.16',
            'Connection': 'keep-alive',
            'Authorization': self.token,
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Sec-Fetch-Mode': 'cors',
        }
        url = 'https://hms.cignacmb.com/health/app/healthTasks/syncUserTaskStep'
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response_json["statusCode"] == '0':
            print('✅步数同步成功')
        else:
            print('❌步数同步失败, ', response_json['msg'])

    def init_guess_coin(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.25.16;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjdGNURDRTMzNEU4N0FGQzZCMTIyQTdEN0U2RTlFN0E4Njc2MTE2IiwibG9naW5UaW1lIjoiMTcyMjgzNzMwMTcwMSIsIm5iZiI6MTcyMjgzNzMwMSwiZXhwdCI6MTcyMjkyMzcwMTcwMiwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyNDA0NjkwMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcyMjgzNzMwMX0.ivNa7mCgxN5TREjRhywD8jBmJWA8kyDs1TUhIrP-K6A;',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/index.html?appVersion=5.25.16',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }
        data = {
            'param': 'e30=',
        }
        url = 'https://member.cignacmb.com/shop/member/interface/initScoreCoin'
        response_json = requests.post(url, headers=headers, data=data).json()
        if response_json["respCode"] == '00':
            remain_count = response_json["respData"]["remainCount"]
            self.guess_coin_count = remain_count
        else:
            print('❌猜硬币初始化失败, ', response_json['respDesc'])

    def guess_coin(self):
        headers = {
            'Host': 'member.cignacmb.com',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'hideLoading': 'true',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://member.cignacmb.com',
            'Referer': 'https://member.cignacmb.com/mb-web/shop/mod/index.html?appVersion=5.25.16',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;hmsapp/5.25.16;HMS_APP_SESSIONID/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWduRGF0YSI6IjdGNURDRTMzNEU4N0FGQzZCMTIyQTdEN0U2RTlFN0E4Njc2MTE2IiwibG9naW5UaW1lIjoiMTcyMjgzNzMwMTcwMSIsIm5iZiI6MTcyMjgzNzMwMSwiZXhwdCI6MTcyMjkyMzcwMTcwMiwiaXNzIjoiSldUIiwiZnJvbSI6IkFQUCIsImV4cCI6MTcyNDA0NjkwMSwidXNlcklkIjoiNzE4MTgwNSIsImlhdCI6MTcyMjgzNzMwMX0.ivNa7mCgxN5TREjRhywD8jBmJWA8kyDs1TUhIrP-K6A;',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
        }
        # Base64编码
        param_dict = {'typeId': '1'}  # 1|9 2|99 3|999
        param_str = json.dumps(param_dict)
        param_bytes = param_str.encode('utf-8')
        encoded_param = base64.b64encode(param_bytes).decode('utf-8')
        data = {
            'param': encoded_param,
        }
        url = 'https://member.cignacmb.com/shop/member/interface/betScoreCoin'
        response_json = requests.post(url, headers=headers, data=data).json()
        if response_json["respCode"] == '00':
            rewardScore = int(response_json["respData"]["rewardScore"])
            print(f'✅猜硬币成功|获得{rewardScore}糯米')
        else:
            print('❌猜硬币失败, ', response_json['respDesc'])

    def main(self):
        if self.user_login():
            self.points_info()
            self.init_lottery()
            time.sleep(random.randint(5, 10))

            # 健康任务
            print(f"\n======== ▷ 健康任务 ◁ ========")
            self.healthy_task()
            time.sleep(random.randint(5, 10))

            # 一诺庄园
            print(f"\n======== ▷ 一诺庄园 ◁ ========")
            self.do_candy_task()
            time.sleep(random.randint(5, 10))
            # 投喂糖果
            self.invest_candy()
            self.init_user_info()
            time.sleep(random.randint(5, 10))

            # 步数挑战
            # print(f"\n======== ▷ 步数挑战 ◁ ========")
            # self.sync_user_step()
            # self.keep_step_challenge()
            # time.sleep(random.randint(5, 10))

            # 猜硬币
            print(f"\n======== ▷ 每天猜硬币 ◁ ========")
            self.init_guess_coin()
            for i in range(int(self.guess_coin_count)):
                self.guess_coin()
                time.sleep(random.randint(5, 10))

            # 糯米转盘(攒一次5连抽吧)
            print(f"\n======== ▷ 糯米大转盘 ◁ ========")
            if int(self.total_score) >= 495:
                for i in range(int(self.lottery_count)):
                    self.do_lottery()
                    time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    env_name = 'ZSXN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"招商信诺共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        ZSXN(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
