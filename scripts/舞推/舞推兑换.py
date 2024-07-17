import requests

headers = {
    'authority': 'wtmall-outside-pro.singworld.net',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer fVqClbvo4-73EiFwt3GPlSQlgLpTANXOa-kdGY8nSGA.x2Udr751GtuggBJ9Q_XWIgwCT1bpdLrnzVkMtbU8cAc',
    'content-type': 'application/json',
    'platform': '1',
    'referer': 'https://servicewechat.com/wx2122a51d44658e18/382/page-frame.html',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'uid': '1096284391',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555',
    'user_token': 'fVqClbvo4-73EiFwt3GPlSQlgLpTANXOa-kdGY8nSGA.x2Udr751GtuggBJ9Q_XWIgwCT1bpdLrnzVkMtbU8cAc',
    'xweb_xhr': '1',
}

json_data = {
    'page': 1,
    'rows': 10,
    'sortType': 0,
    'shopId': 0,
    'uid': 1096284391,
    'platformId': 1,
}

response = requests.post('https://wtmall-outside-pro.singworld.net/wtmall/shop/index', headers=headers, json=json_data)
response_json = response.json()
if response_json['code'] == 0:
    list = response_json['data']['list']

