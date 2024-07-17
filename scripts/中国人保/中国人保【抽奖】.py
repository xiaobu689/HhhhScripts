"""
中国人保【抽奖】

超级1+6|每周一、周六、每月尾数逢1，逢6抽奖

变量名: ZGRBCJ
变量： openid，多账号&连接
微信公众号福建人保财险，菜单栏超级1+6抓包openid
cron: 35 6 * * *
const $ = new Env("中国人保【抽奖】");
"""
import os
from datetime import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from sendNotify import send


def lottery(openid_list, activity_id):
    for s, openid in enumerate(openid_list):
        login_data = {
            "requestbody": {
                "comCode": "",
                "userName": "",
                "comId": "",
                "agentCode": "0",
                "userId": "picc-fuj",
                "unionId": "",
                "openId": openid
            }
        }
        response = requests.post("https://smsp.epicc.com.cn/WAS/userLoginApi/autoLogin", json=login_data, verify=False)
        login_result = response.json()
        unionid = login_result['data'].get('unionid', '')
        name = login_result['data'].get('encryName', '')

        activity_data = {
            "header": {
                "openid": openid,
                "comCode": "35000000",
                "comId": "35000000",
                "userName": name,
                "agentCode": "0",
                "token": "",
                "userId": "picc-fuj",
                "unionId": unionid
            },
            "body": {
                "cmd": "queryactivitydetail",
                "activityNo": activity_id,
                "memId": "",
                "activityType": "1",
                "transactionNo": "",
                "isDifferWinningRate": ""
            }
        }
        response = requests.post("http://smsp.epicc.com.cn/WAS/recentActivtyApi/themeActivityNew", json=activity_data,
                                 verify=False)
        activity_result = response.json()
        msg = activity_result.get('message', '')
        activity_name = activity_result['data'].get('activityName', '')
        gift_name = activity_result['data'].get('giftName', '')

        if "很遗憾" in gift_name or gift_name is None:
            print(f"{s}没中")
        else:
            print(f"{s} {msg} {activity_name} {gift_name}")
            msg = f"福建人保财险账号{s}中了{gift_name}"
            send("福建人保中奖", msg)
            print(msg)


if __name__ == "__main__":
    rbcx = os.getenv('rbcx', '')
    openid_list = rbcx.split('&')
    today = datetime.today()
    weekday = today.weekday() + 1
    day = today.day

    if weekday == 1:
        activity_id = "300008404"
        lottery(openid_list, activity_id)
    elif weekday == 6:
        activity_id = "300008402"
        lottery(openid_list, activity_id)

    if str(day)[-1] == '1':
        activity_id = "300008458"
        lottery(openid_list, activity_id)
    elif str(day)[-1] == '6':
        activity_id = "300008348"
        lottery(openid_list, activity_id)
    else:
        print("今日非活动日期")
