"""
叮咚鱼塘
定时设置：
cron: 33 7,12,19 * * *
const $ = new Env("叮咚鱼塘");
"""
import os
import random
import re
import time
import requests

from sendNotify import send


def sign_ddyt(i, cookie):
    message = ""
    message_name = "骑狗跨大海"
    message_success = f'✅帐号：{i}\n'
    message_fail = f'❌帐号：{i}'
    seed_id = 201004000232285148
    props_id = 201004000233063148
    # 领取任务奖励
    user_task_log_id = []
    headers = {
        'Host': 'farm.api.ddxq.mobi',
        'Origin': 'https://game.m.ddxq.mobi',
        'Cookie': cookie,
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://game.m.ddxq.mobi/',
    }
    # 请求头
    headerintegral = {
        'Host': 'sunquan.api.ddxq.mobi',
        'Cookie': cookie,
        'Referer': 'https://activity.m.ddxq.mobi/',
        'ddmc-city-number': '0201',
        'ddmc-api-version': '9.7.3',
        'Origin': 'https://activity.m.ddxq.mobi',
        'ddmc-build-version': '10.15.0',
        'ddmc-longitude': '114.345477',
        'ddmc-latitude': '40.123389',
        'ddmc-app-client-id': '3',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'ddmc-station-id': '',
        'ddmc-ip': '',
    }

    # 请求数据
    dataintegral = {
        'api_version': '9.7.3',
        'app_client_id': '3',
        'app_version': '2.14.5',
        'app_client_name': 'activity',
        'station_id': '',
        'native_version': '10.15.0',
        'city_number': '0201',
        'device_token': '',
        'device_id': '',
        'latitude': '40.123389',
        'longitude': '116.345477',
    }

    # 请求URL
    url = 'https://sunquan.api.ddxq.mobi/api/v2/user/signin/'

    # 发送POST请求
    resp = requests.post(url, headers=headerintegral, data=dataintegral)
    if resp.status_code == 200:
        resp_json = resp.json()
        print(resp_json)
        code = resp_json["code"]
        msg = resp_json["msg"]
        if code == 0:
            message_success += f'✅签到结果：积分签到成功\n'
            print("✅帐号：" + message_name + "积分签到成功 ")
        else:
            message_fail += f'❌签到结果：积分签到失败\n'
            print("❌帐号：" + message_name + msg + " ")
    else:
        print(resp.text)
        message_fail += '❌签到结果：积分签到失败\n'
        print("✅帐号：" + message_name + "积分签到失败 ")

    flag_sign = 0  # 标识是否签到领取饲料
    temp_message_fail = ""  # 记录临时失败的消息

    resp = requests.get(
        "https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.1.0&app_client_id=1&station_id=&stationId=&native_version=&app_version=10.15.0&OSVersion=15&CityId=0201&uid=&latitude=40.123389&longitude=116.345477&lat=40.123389&lng=116.345477&device_token=&gameId=1&taskCode=DAILY_SIGN",
        headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        print(resp_json)
        code = resp_json["code"]
        msg = resp_json["msg"]
        if code == 0:
            flag_sign = 1
            print("✅签到结果：鱼塘签到成功\n")
        else:
            print("✅帐号：" + message_name + msg + " ")
    else:
        print(resp.text())
        print("帐号：" + message_name + "签到失败 ")

    resp = requests.get(
        "https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.1.0&app_client_id=1&station_id=&stationId=&native_version=&app_version=10.1.2&OSVersion=15&CityId=0201&uid=&latitude=40.123389&longitude=116.345477&lat=40.123389&lng=116.345477&device_token=&gameId=1&taskCode=CONTINUOUS_SIGN",
        headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        print(resp_json)
        code = resp_json["code"]
        msg = resp_json["msg"]
        if code == 0:
            flag_sign = 1
            print("✅帐号：" + message_name + "鱼塘签到成功\n ")
        else:
            temp_message_fail = "帐号：" + message_name + msg + " "
            print("帐号：" + message_name + msg + " ")
    else:
        print(resp.text())
        temp_message_fail = "帐号：" + message_name + "签到失败 "
        print("帐号：" + message_name + "签到失败 ")

    if flag_sign == 1:
        message_success += "✅签到结果：鱼塘签到成功\n"
    else:
        message_fail += temp_message_fail

    # 获取任务taskCode
    task_code = []
    # 获取任务列表
    resp = requests.get(
        "https://farm.api.ddxq.mobi/api/v2/task/list?latitude=40.123389&longitude=116.345477&env=PE&station_id=&city_number=0201&api_version=9.44.0&app_client_id=3&native_version=10.15.0&h5_source=&page_type=2&gameId=1",
        headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        code = resp_json["code"]
        if code == 0:
            print("正在获取taskCode ")
            user_tasks = resp_json["data"]["userTasks"]
            for task in user_tasks:
                task_code.append(task["taskCode"])  # 将 task["taskCode"] 添加到 task_code 列表中
            print(task_code)
        else:
            print("获取taskCode失败 ")
    else:
        print(resp.text())
        print("获取taskCode失败 ")

    # 完成任务
    if len(task_code) > 0:
        print("尝试完成任务...")
        for j in range(len(task_code)):
            url_task = "https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.1.0&app_client_id=1&station_id=&stationId=&native_version=&app_version=10.15.0&OSVersion=15&CityId=0201&uid=&latitude=40.123389&longitude=116.345477&lat=40.123389&lng=116.345477&device_token=&gameId=1&taskCode=" + \
                       task_code[j]
            try:
                resp = requests.get(url_task, headers=headers)
                time.sleep(2)
            except:
                print("忽略任务：" + task_code[j])
        print("任务完成...")
    # -------------------------------------------------------
    # 获取奖励id
    user_task_log_id = []
    resp = requests.get(
        "https://farm.api.ddxq.mobi/api/v2/task/list?latitude=40.123389&longitude=116.345477&env=PE&station_id=&city_number=0201&api_version=9.44.0&app_client_id=3&native_version=10.15.0&h5_source=&page_type=2&gameId=1",
        headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        code = resp_json["code"]
        if code == 0:
            print("正在获取userTaskLogId ")
            user_tasks = resp_json["data"]["userTasks"]
            for task in user_tasks:
                temp = task.get("userTaskLogId")
                if isinstance(temp, str) and len(temp) == 18:
                    user_task_log_id.append(temp)  # 将值添加到列表中
        else:
            print("获取userTaskLogId失败 ")
    else:
        print(resp.text())
        print("获取userTaskLogId失败 ")

    # 领取任务奖励
    if len(user_task_log_id) > 0:
        print("尝试领取任务奖励...")
        for j in range(len(user_task_log_id)):
            url_task = "https://farm.api.ddxq.mobi/api/v2/task/reward?api_version=9.1.0&app_client_id=1&station_id=&stationId=&native_version=&app_version=10.15.1&OSVersion=15&CityId=0201&uid=&latitude=40.123389&longitude=116.345477&lat=40.123389&lng=116.345477&device_token=&userTaskLogId=" + \
                       user_task_log_id[j]
            try:
                resp = requests.get(url_task, headers=headers)
                time.sleep(2)
            except:
                print("忽略任务：" + user_task_log_id[j])
        print("任务奖励领取完成...")
    # 喂饲料
    amount = 10  # 记录剩余数目
    amout_count = 0  # 已喂饲料次数
    flag_amount = 0  # 标志，1为饲料
    count_seed_id = 0  # 计算是不是每次浇花的剩余水量都一样，如果三次都一样，则认为seedid过期
    last_amount = 0  # 记录上一次剩余水量
    while amount >= 10:
        url = f"https://farm.api.ddxq.mobi/api/v2/props/feed?api_version=9.1.0&app_client_id=1&station_id=&stationId=&native_version&app_version=10.0.1&OSVersion=15&CityId=0201&uid=&latitude=40.123389&longitude=116.345477&lat=40.123389&lng=116.345477&device_token=&gameId=1&propsId={props_id}&seedId={seed_id}&cityCode=0201&feedPro=0&triggerMultiFeed=1"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp_json = resp.json()
            code = resp_json["code"]
            msg = resp_json["msg"]
            if code == 0:
                amount = resp_json["data"]["props"]["amount"]
                if last_amount == amount:
                    count_seed_id += 1
                else:
                    count_seed_id = 0
                last_amount = amount
                if count_seed_id >= 3:
                    msg = "[❗❗❗提醒]seedId值可能过期，请抓包获取最新的值"
                    message_fail += "[❗❗❗提醒]seedId值可能过期，请抓包获取最新的值"
                    print("提前退出浇水，错误消息为：" + msg)
                    amout_count -= 3
                    break
                flag_amount = 1
                amout_count += 1
                print("喂饲料中... ,剩余饲料：" + str(amount))
            else:
                print(resp.json())
                print("提前退出喂饲料，错误消息为：" + msg)
                amount = 0
        else:
            print(resp.text())
            print("提前退出喂饲料")
            amount = 0

    if flag_amount == 1:
        message_success += "✅成功喂饲料" + str(amout_count) + "次\n"
        print("成功喂饲料" + str(amout_count) + "次 ")
    else:
        message_fail += "喂饲料日志：" + msg + "\n"
        print("喂饲料日志：" + msg + " ")

    message += message_fail + " " + message_success
    print("推送信息：", message)
    # 推送
    send("叮咚鱼塘", message)
    print('脚本执行完毕.')


if __name__ == '__main__':
    env_name = 'DDYT'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"叮咚鱼塘共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        sign_ddyt(i, token)
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(10, 15))


