
"""
中国人保【种菜】

微信小程序picc爱心农场nongchang.maxrocky.com，抓包skey
变量名: ZGRBZC
cron: 51 8 * * *
const $ = new Env("中国人保【种菜】");
"""
import os
import requests
import json
import time
from datetime import datetime

def buy(s, skey, buyid, url):
    data = {
        "skey": skey,
        "type": "seeds",
        "buyId": buyid,
        "num": 1
    }
    response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FbuyGoods", json=data, verify=False)
    msg = response.json().get('errMsg', '')
    time.sleep(1)
    if "购买成功" in msg:
        plant_data = {
            "skey": skey,
            "seedId": buyid,
            "lid": i
        }
        plant_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FuserCrops", json=plant_data,
                                       verify=False)
        print(f"账号{s}种植 {plant_response.json().get('errMsg', '')}")
        time.sleep(1)

        for action, action_name in [("wateringCrops", "浇水"), ("fertilizeCrops", "施肥"), ("weedCrops", "除草"),
                                    ("killDebug", "除虫")]:
            action_data = {
                "type": action,
                "skey": skey,
                "lid": i
            }
            action_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog", json=action_data,
                                            verify=False)
            print(f"账号{s}{action_name} {action_response.json().get('errMsg', '')}")
            time.sleep(1)
    elif "已售完" in msg or "等级不足" in msg or "每日最多" in msg:
        print(f"购买{buyid}种子失败 {msg}")
        if buyid == 11:
            print(f"失败次数过多跳过账号{s}")
            return False
        buyid -= 1
        buy(s, skey, buyid, url)
    elif "太频繁了" in msg:
        print(f"稍等一会 {msg}")
        time.sleep(61)
        buy(s, skey, buyid, url)

    return True


# Main script
if __name__ == "__main__":
    rbnc = os.getenv('rbnc', '')
    ck = rbnc.split('&')
    url = "nongchang.maxrocky.com"
    current_hour = datetime.now().hour
    current_weekday = datetime.now().isoweekday()

    for s, skey in enumerate(ck):
        response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog",
                                 json={"type": "harvestFruitAll", "skey": skey, "order_id": 1}, verify=False)
        print(f"账号{s}一键收获 {response.json().get('errMsg', '')}")
        time.sleep(1)

        response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FshovelFruit", json={"skey": skey},
                                 verify=False)
        print(f"账号{s}一键铲除 {response.json().get('errMsg', '')}")
        time.sleep(1)

        response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FuserSell",
                                 json={"sellType": "fruit", "type": "all", "skey": skey}, verify=False)
        print(f"账号{s}出售 {response.json().get('errMsg', '')}")
        time.sleep(1)

        response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FgetUserSeed", json={"skey": skey},
                                 verify=False)
        user_data = response.json()
        level = int(user_data['data']['level'])
        lands = min(level + 1, 9)
        land = [int(x.split(':')[1]) for x in user_data['data']['landId'].split(',')]
        landed = sorted(set(range(1, lands + 1)) - set(land))

        buyid = level + 12

        if current_weekday == 1:
            for task in ["userSell", "upgradeReminder", "returnReward", "helpFriends", "getbablance", "LiveStreaming"]:
                task_data = {"type": task, "skey": skey}
                task_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog", json=task_data,
                                              verify=False)
                print(f"账号{s}执行任务 {task} {task_response.json().get('errMsg', '')}")
                time.sleep(1)

        if current_hour < 3:
            for lid in range(1, lands + 1):
                water_data = {"type": "wateringCrops", "skey": skey, "lid": lid}
                water_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog", json=water_data,
                                               verify=False)
                print(f"账号{s}浇水 {water_response.json().get('errMsg', '')}")
                time.sleep(1)

            dog_data = {"skey": skey, "type": "decate", "buyId": 12, "num": 2}
            dog_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FbuyGoods", json=dog_data,
                                         verify=False)
            print(f"账号{s}购买狗💩 {dog_response.json().get('errMsg', '')}")

            achieve_data = {"skey": skey}
            achieve_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FgetUserDonateExtraLog",
                                             json=achieve_data, verify=False)
            print(f"账号{s}完成成就 {achieve_response.json().get('errMsg', '')}")
            time.sleep(1)

            for task in ["BrowseYouyang", "CourtesyPets", "awardShare", "dogfood", "harvestFruitShare", "shareTimeline",
                         "sign", "LovePets"]:
                task_data = {"type": task, "skey": skey}
                task_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog", json=task_data,
                                              verify=False)
                print(f"账号{s}执行任务 {task} {task_response.json().get('errMsg', '')}")
                time.sleep(1)

            for _ in range(3):
                for task in ["edproducts", "recall", "invition"]:
                    task_data = {"type": task, "skey": skey,
                                 "edproducts_name": "人保寿险美满鑫家年金保险(分红型)"} if task == "edproducts" else {
                        "type": task, "skey": skey}
                    task_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog",
                                                  json=task_data, verify=False)
                    print(f"账号{s}执行任务 {task} {task_response.json().get('errMsg', '')}")
                    time.sleep(1)

            for _ in range(6):
                water_friend_data = {"type": "wateringByFriends", "skey": skey}
                water_friend_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog",
                                                      json=water_friend_data, verify=False)
                print(f"账号{s}执行任务 wateringByFriends {water_friend_response.json().get('errMsg', '')}")
                time.sleep(1)

            question_data = {"type": "questionBank", "skey": skey, "type_id": 9, "userAnswer": "A"}
            question_response = requests.post(f"https://{url}/index.php?s=index%2Findex%2FsetUserLog",
                                              json=question_data, verify=False)
            print(f"账号{s}执行任务 questionBank {question_response.json().get('errMsg', '')}")
            time.sleep(1)

        for i in landed:
            if not buy(s, skey, buyid, url):
                break

        print("........................................")
