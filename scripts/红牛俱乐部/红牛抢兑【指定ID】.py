"""
红牛抢兑【动态获取】

变量名: RedBull

cron: 58 13 * * 5
const $ = new Env("红牛抢兑【动态获取】");

20240708 不确定商品上新E卡ID是否会变，准备2个本，一个指定ID，一个动态获取
--------------------------------------------
每周五 14:00积分兑换商品上新
--------------------------------------------
商品：网易云音乐黑胶会员月卡 需要积分：744，id：313
商品：喜茶代金券20元 需要积分：1297，id：312
商品：盒马鲜生电子卡20元 需要积分：1342，id：311
商品：猫眼电影代金券20元 需要积分：1386，id：310
商品：猫眼电影代金券10元 需要积分：693，id：309
商品：京东E卡30元 需要积分：2013，id：308
商品：京东E卡10元 需要积分：671，id：307
商品：天猫超市享淘卡20元 需要积分：1304，id：306
商品：天猫超市享淘卡10元 需要积分：652，id：305
"""

import datetime
import asyncio
import json
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
        # else:
        #     print(f"当前时间: {now.hour}:{now.minute}:{now.second}.{now.microsecond // 1000}")
        await asyncio.sleep(0)


async def exchange(redbull_token):
    headers = {
        'Connection': 'keep-alive',
        'X-VERSION': '2.1.2',
        'Authorization': 'bearer ' + redbull_token,
        'HH-VERSION': '0.2.2',
        'MARKETING-PLAN-NO': '',
        'ONE-ID': ' ',
        'HH-FROM': '20230522308440',
        'componentSend': '1',
        'HH-APP': 'wx5549b5fa9842e321',
        'USER-ENTRANCE-CHANNEL': '',
        'appPublishType': '1',
        'USER-ENTRANCE-CHANNEL-KEY': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080712) XWEB/1191',
        'groupPosId': '',
        'Content-Type': 'application/json;charset=UTF-8',
        'xweb_xhr': 1,
        'store': ',:,',
        'HH-CI': 'saas-wechat-app',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx5549b5fa9842e321/35/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    # 10元E卡
    itemId = '7206555082813784064'
    activityNo = '307'
    body = {
        "businessType": "POINTS_MALL",
        "pointMallSubmitRequest": {
            "exchangeActivityId": activityNo,
            "productBizNo": itemId,
            "discountType": "VIRTUAL"
        }
    }
    body_json = json.dumps(body)
    url = 'https://xiaodian.miyatech.com/api/order/center/order/submit'
    start_time = time.time()
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(url, data=body_json) as response:
                end_time = time.time()
                end_response = datetime.now()
                duration_ms = (end_time - start_time) * 1000

                data = await response.json()
                if data.get('success'):
                    message = f"✅ 兑换成功 | {data['message']} | 耗时: {duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                else:
                    message = f"❌ 兑换失败 | {data['message']} | 耗时：{duration_ms:.2f} ms | 响应时间：{end_response.strftime('%H:%M:%S.%f')[:-3]}"
                print(message)
                return message
        except Exception as e:
            error_message = f"请求异常：{e}"
            print(error_message)
            return error_message

async def main():
    messages = []  # 用于存储每次提现操作的消息
    tokenStr = os.getenv('SYCC_TOKEN')
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {tokenStr} 是否填写')
        return

    # 第一个账号参与抢兑
    try:
        json_data = json.loads(tokenStr)
        print(f"共获取到{len(json_data)}个账号")
    except json.JSONDecodeError:
        print('⛔️ JSON 解析失败，请检查变量格式是否正确')
        exit(0)
    redBull_token = json_data[0]

    now = datetime.now()
    if now.hour in [13]:
        target_hour = now.hour
    else:
        print("⚠️ 当前时间不在抢购时间段内。")
        return

    await trigger_at_specific_millisecond(target_hour, 59, 59, 830)

    tasks = [exchange(redBull_token) for _ in range(10)]
    results = await asyncio.gather(*tasks)

    for result in results:
        messages.append(result)

    # 消息推送
    send("红牛抢兑结果通知", "\n".join(messages))


if __name__ == '__main__':
    asyncio.run(main())
