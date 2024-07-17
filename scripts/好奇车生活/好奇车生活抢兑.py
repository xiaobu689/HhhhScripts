"""
好奇车生活抢兑

【单号版】
抓任意包请求头 openId 和 accountId
变量名:  Cheryfs
变量格式：openId#accountId
多账号用&分割

cron: 58 17 * * *
const $ = new Env("好奇车生活抢兑");
"""

"""
限时福利（每天18:00开抢）
--------------------
🌼兑换商品：京东E卡18元        | id:792556957722198016 兑换所需积分：1800
🌼兑换商品：美团外卖代金券10元   | id:792556468305641472 兑换所需积分：750
🌼兑换商品：3.88元红包         | id:754493262869991424 兑换所需积分：588
🌼兑换商品：5.88元红包         | id:754493011522113536 兑换所需积分：888
🌼兑换商品：1.08元红包         | id:754492665391370240 兑换所需积分：188
🌼兑换商品：单次洗车券          | id:812852940045557760 兑换所需积分：3000
🌼兑换商品：高德打车5元代金券    | id:792555679986204672 兑换所需积分：375
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


async def exchange(account_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF',
        'tenantId': '619669306447261696',
        'activityId': '621950054462152705',
        'accountId': account_id,
    }

    # 5.88元红包构造参数
    # pointsMallCardId = '754493011522113536'
    # exchangeNeedPoints = 888

    # 18元京东E卡构造参数
    pointsMallCardId = '792556957722198016'
    exchangeNeedPoints = 1800
    exchangeCount = 1
    exchangeType = 0
    exchangeNeedMoney = 0

    url = f'https://channel.cheryfs.cn/archer/activity-api/pointsmall/exchangeCard?pointsMallCardId=${pointsMallCardId}&exchangeCount=${exchangeCount}&mallOrderInputVoStr=%7B%22person%22:%22%22,%22phone%22:%22%22,%22province%22:%22%22,%22city%22:%22%22,%22area%22:%22%22,%22address%22:%22%22,%22remark%22:%22%22%7D&channel=1&exchangeType=${exchangeType}&exchangeNeedPoints=${exchangeNeedPoints}&exchangeNeedMoney=${exchangeNeedMoney}&cardGoodsItemIds='
    start_time = time.time()
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as response:
                # 计算接收响应的时间
                end_time = time.time()
                end_response = datetime.now()  # 记录收到响应的当前时间
                duration_ms = (end_time - start_time) * 1000

                data = await response.json()
                if data["code"] == 200:
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
    messages = []  # 用于存储每次提现操作的消息
    cheryfs = os.getenv('Cheryfs')
    cheryfs = 'oqX_y5Y_FfcApLTeAcmHX4R_kQ6E#efddacbbbdd70a7f2f77498ed59afe298c5b7e31489a3a4ca5beeffceafcd63f'
    if not cheryfs:
        print(f'⛔️未获取到ck变量：请检查变量 {cheryfs} 是否填写')
        return

    # 第一个参与抢兑
    tokens = re.split(r'&', cheryfs)
    _token = tokens[0]
    account_id = re.split(r'#', _token)[1]

    now = datetime.now()
    if now.hour in [17]:
        target_hour = now.hour
    else:
        print("⚠️ 当前时间不在抢购时间段内。")
        return

    await trigger_at_specific_millisecond(target_hour, 59, 59, 600)

    tasks = [exchange(account_id) for _ in range(10)]
    results = await asyncio.gather(*tasks)

    for result in results:
        messages.append(result)

    # 消息推送
    send("好奇车生活抢兑结果通知", "\n".join(messages))


if __name__ == '__main__':
    asyncio.run(main())
