import requests
print("活动时间：7.1-7.31, 积分攒不够了，先不写")
exit(0)
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': 'bearer b9e7e74c-617a-4d09-af4a-615628f32e9d',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'HH-APP': 'wxb33ed03c6c715482',
    'HH-CI': 'saas-wechat-app',
    'HH-FROM': '20230130307725',
    'HH-VERSION': '0.2.8',
    'MARKETING-PLAN-NO': '',
    'ONE-ID': '',
    'Referer': 'https://servicewechat.com/wxb33ed03c6c715482/28/page-frame.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'USER-ENTRANCE-CHANNEL': '',
    'USER-ENTRANCE-CHANNEL-KEY': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555',
    'X-VERSION': '2.1.3',
    'appPublishType': '1',
    'componentSend': '1',
    'groupPosId': '',
    'store': ',:,',
    'xweb_xhr': '1',
}

params = {
    'categoryId': '41',
    'pageNo': '1',
    'pageSize': '10',
    'sortKey': '',
    'sortVal': '',
    'screenExGoods': 'DISABLE',
}

response = requests.get(
    'https://xiaodian.miyatech.com/api/coupon/integral-mall/exchange-item/query',
    params=params,
    headers=headers,
)
response_json = response.json()
if response_json['code'] == 200:
    list = response_json['data']['resultList']
    for item in list:
        name = item['name']
        availableCount = item['availableCount']
        exchangeIntegral = item['exchangeIntegral']