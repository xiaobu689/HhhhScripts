"""
上海徐汇E卡抢兑

【单号版】
点击积分兑换进入商场，抓商品列表请求头 Authorization
变量名: SHXHKC_TOKEN

--------------------------
20240624 E卡每周二10点抢兑，面值：5元|10元---兑换周期【2024.3.1-2024.8.31】
--------------------------

cron: 58 9 * * 2
const $ = new Env("上海徐汇E卡抢兑");
"""
import datetime
import asyncio
import os
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
        await asyncio.sleep(0)  # 让出控制权给其他任务


async def exchange(token):
    headers = {
        'Host': 'mall-api.shmedia.tech',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': token,
        'Sec-Fetch-Site': 'same-site',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://mall-mobile.shmedia.tech',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Rmt/XuHui; Version/2.3.5',
        'Referer': 'https://mall-mobile.shmedia.tech/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty'
    }
    base_url = 'https://mall-api.shmedia.tech/trade-service/trade/carts/buy'
    params = {
        'sku_id': '1551455924135903234',
        'num': '1',
        'activity_id': '1763439141567246338',
        'promotion_type': 'EXCHANGE'
    }
    url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    tasks = []
    start_time = time.time()  # 记录开始发送请求的时间
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers) as response:
                # 计算接收响应的时间
                end_time = time.time()
                end_response = datetime.now()  # 记录收到响应的当前时间
                duration_ms = (end_time - start_time) * 1000

                data = await response.json()
                if data["code"] == '0':
                    message = f"✅ 抢兑成功 | {data['message']} | 耗时: {duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                else:
                    message = f"❌ 抢兑失败 | {data['message']} | 耗时：{duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                print(message)
                return message
        except Exception as e:
            error_message = f"请求异常：{e}"
            print(error_message)
            return error_message


async def main():
    messages = []  # 用于存储每次提现操作的消息
    token = os.getenv('SHXHKC_TOKEN')
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {token} 是否填写')
        return
    now = datetime.now()
    # 根据当前小时设置目标时间
    if now.hour in [9]:
        target_hour = now.hour
    else:
        print("⚠️ 当前时间不在抢购时间段内。")
        return
    await trigger_at_specific_millisecond(target_hour, 59, 59, 830)

    tasks = [exchange(token) for _ in range(10)]
    results = await asyncio.gather(*tasks)
    for result in results:
        messages.append(result)

    # 消息推送
    send("上海徐汇抢兑结果通知", "\n".join(messages))


if __name__ == '__main__':
    asyncio.run(main())
