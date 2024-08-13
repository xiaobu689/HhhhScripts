"""
顺义创城抢兑【多账号】

【多账号版】
抓任意包请求头 x_applet_token
变量名: SYCC_TOKEN

cron: 58 7,11,19 * * *
const $ = new Env("顺义创城抢兑【多账号】");
-------------------------------
20240813 增加代理配置，测试不用代理也可以到账，避免后面接口升级，懒得经常查看
-------------------------------
"""

import csv
import json
import datetime
import asyncio
import os
import re
import time
from datetime import datetime
import aiohttp

from pinzan_proxy import pinzan_proxy
from sendNotify import send


async def trigger_at_specific_millisecond(hour, minute, second, millisecond):
    target_time = hour * 60 * 60 * 1000 + minute * 60 * 1000 + second * 1000 + millisecond
    while True:
        now = datetime.now()
        current_time = now.hour * 60 * 60 * 1000 + now.minute * 60 * 1000 + now.second * 1000 + now.microsecond // 1000
        if current_time >= target_time:
            break
        await asyncio.sleep(0)


async def cashout(token, phone, api_proxies):
    headers = {
        'Host': 'admin.shunyi.wenming.city',
        'Connection': 'keep-alive',
        'X-Applet-Token': token,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x1800312c) NetType/WIFI Language/zh_CN',
    }
    url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/award/exchangeAward'
    start_time = time.time()
    # 请求体
    # 1562334019131645953|2元
    # 1788826595521810434|1元
    payload = {
        "awardIds": ["1788826595521810434"],
        "phone": phone
    }
    # 创建一个空的 data 字典
    body = json.dumps(payload)
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            # 配置代理
            async with session.post(url, data=body, proxy=api_proxies) as response:
                end_time = time.time()
                end_response = datetime.now()
                duration_ms = (end_time - start_time) * 1000
                data = await response.json()
                if data.get('success'):
                    message = f"✅ {phone} | 提现成功 | {data['message']} | 耗时: {duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                else:
                    message = f"❌ {phone} | 提现失败 | {data['message']} | 耗时：{duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                print(message)
                return message
        except Exception as e:
            error_message = f"请求异常：{e}"
            print(error_message)
            return error_message


def get_success_phones():
    today_date = datetime.now().strftime("%Y%m%d")
    file_name = f'sycc_tx_success_{today_date}.csv'
    existing_phones = set()
    with open(file_name, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            existing_phones.add(row[0])
    return existing_phones


async def main():
    messages = []
    SY_token = os.getenv('SYCC_QD')
    if not SY_token:
        print(f'⛔️未获取到ck变量：请检查变量 {SY_token} 是否填写')
        return
    tokens = re.split(r'&', SY_token)
    existing_phones = get_success_phones()
    tokens_ = []
    tar_millisecond = 0
    for i, token in enumerate(tokens, start=1):
        auth, phone, millisecond = token.split('#')
        if i == 1:
            tar_millisecond = millisecond
        if phone not in existing_phones:
            tokens_.append(token)
    # 生成代理
    proxies = pinzan_proxy(len(tokens_), 1, '110100')

    now = datetime.now()
    if now.hour in [7, 11, 19]:
        target_hour = now.hour
    else:
        print("⚠️ 当前时间不在抢购时间段内。")
        return
    await trigger_at_specific_millisecond(target_hour, 59, 59, int(tar_millisecond))

    tasks = []
    for i, token in enumerate(tokens_, start=1):
        token, phone, millisecond = token.split('#')
        for _ in range(1):
            api_proxies = proxies[i - 1].get('https')
            tasks.append(cashout(token, phone, api_proxies))

    results = await asyncio.gather(*tasks)
    for result in results:
        if "提现成功" in result:
            phone_pattern = r'\b1[3-9]\d{9}\b'
            match = re.search(phone_pattern, result)
            if match:
                phone_number = match.group()
                today_date = datetime.now().strftime("%Y%m%d")
                file_name = f'sycc_tx_success_{today_date}.csv'
                with open(file_name, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([phone_number])
                print(f"✅ 抢兑成功，手机号 {phone_number} 已记录到 sycc_tx_success.csv 文件中")
        messages.append(result)

    # 消息推送
    send("顺义创城抢兑结果通知", "\n".join(messages))


if __name__ == '__main__':
    asyncio.run(main())
