"""
顺义创城抢兑

【单账号版】
抓任意包请求头 x_applet_token#phone#milliseconds
变量名: SYCC_QD

cron: 58 7,11,19 * * *
const $ = new Env("顺义创城抢兑");
"""

import datetime
import asyncio
import os
import re
import time
from datetime import datetime
import aiohttp
from sendNotify import send


async def trigger_at_specific_millisecond(hour, minute, second, millisecond):
    target_time = hour * 60 * 60 * 1000 + minute * 60 * 1000 + second * 1000 + millisecond
    while True:
        now = datetime.now()
        current_time = now.hour * 60 * 60 * 1000 + now.minute * 60 * 1000 + now.second * 1000 + now.microsecond // 1000
        if current_time >= target_time:
            break
        # else:
        #     print(f"当前时间: {now.hour}:{now.minute}:{now.second}.{now.microsecond // 1000}")
        await asyncio.sleep(0)  # 让出控制权给其他任务


async def cashout(token, phone):
    headers = {
        'Host': 'admin.shunyi.wenming.city',
        'Connection': 'keep-alive',
        'X-Applet-Token': token,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x1800312c) NetType/WIFI Language/zh_CN',
    }
    url = 'https://admin.shunyi.wenming.city/jeecg-boot/applet/award/exchangeAward'
    start_time = time.time()  # 记录开始发送请求的时间
    # 1562334019131645953|2元
    # 1788826595521810434|1元
    body = f'{"awardIds":["1788826595521810434"],"phone":{phone}}'
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(url, data=body) as response:
                # 计算接收响应的时间
                end_time = time.time()
                # 记录收到响应的当前时间
                end_response = datetime.now()
                duration_ms = (end_time - start_time) * 1000

                data = await response.json()
                if data.get('success'):
                    message = f"✅ 提现成功 | {data['message']} | 耗时: {duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                else:
                    message = f"❌ 提现失败 | {data['message']} | 耗时：{duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                print(message)
                return message
        except Exception as e:
            error_message = f"请求异常：{e}"
            print(error_message)
            return error_message


async def main():
    messages = []
    SY_token = os.getenv('SYCC_TOKEN')
    if not SY_token:
        print(f'⛔️未获取到ck变量：请检查变量 {SY_token} 是否填写')
        return

    # 第一个账号参与抢兑
    tokens = re.split(r'&', SY_token)
    sycc_token = tokens[0]
    token, phone, millisecond = sycc_token.split('#')

    now = datetime.now()
    if now.hour in [7, 11, 19]:
        target_hour = now.hour
    else:
        print("⚠️ 当前时间不在抢购时间段内。")
        return

    await trigger_at_specific_millisecond(target_hour, 59, 59, int(millisecond))

    tasks = [cashout(token, phone) for _ in range(10)]
    results = await asyncio.gather(*tasks)

    for result in results:
        messages.append(result)

    # 消息推送
    send("顺义创城枪兑结果通知", "\n".join(messages))


if __name__ == '__main__':
    asyncio.run(main())
