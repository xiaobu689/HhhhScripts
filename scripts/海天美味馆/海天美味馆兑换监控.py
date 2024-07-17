"""


🐍155 | 腾讯视频VIP会员月卡 | 1000
"""
import requests
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjExODY1NTMsInN1YiI6IkJVWUVSIiwib3BlbklkIjoib2NnNnk0bU5JdlFOQldpTmh0WnI4Q3dPek45RSIsInJvbGVzIjpbIkJVWUVSIl0sImV4cCI6MTcxOTkyOTM4NiwidXVpZCI6InVxZm9nWmVFU3NxTk9GeWJEVFVlIiwidXNlcm5hbWUiOiJtXzkyODUxMzY4NDE3In0.VQcC-_5PqlJg4gJ2bv7YhlCQhSBns5AuInADdMKiVIK90T-Qmx-PofyEfASMlQFY2QdshsbA59iurbXrttgGTQ',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wx7a890ea13f50d7b6/602/page-frame.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129',
    'envVersion': 'release',
    'uuid': 'uqfogZeESsqNOFybDTUe',
    'xweb_xhr': '1',
}


# 用户积分
def user_score():
    response = requests.get('https://cmallapi.haday.cn/buyer-api/members/points/current', headers=headers)
    if not response or response.status_code != 200:
        print("获取积分失败")
        return
    response_json = response.json()
    print(f'🐍积分：{response_json["consum_point"]}')

    return response_json["consum_point"]

# 兑换
def exchange():
    url = 'https://cmallapi.haday.cn/buyer-api/point-mall/cart/buy?point_goods_id=155&num=1&way=POINT_BUY_NOW'
    response = requests.post(url, headers=headers)
    if not response or response.status_code != 200:
        print(f"兑换失败 | {response.text}")
        return
    response_json = response.json()
    if response_json['code'] == 200:
        print("兑换成功")
    else:
        print(f"兑换失败 | {response_json['message']}")

# 腾讯月卡
def tecent_jk():
    response = requests.get('https://cmallapi.haday.cn/buyer-api/point/goods/155', headers=headers)
    if not response or response.status_code != 200:
        print("获取详情失败")
        return
    response_json = response.json()
    if response_json['code'] == 200:
        quantity = response_json['data']['point_goods_vo']["enable_quantity"]
        if quantity > 0 :
            print("监控到腾讯月卡有库存，开始兑换......")
            exchange()
    else:
        print("腾讯视频VIP会员月卡详情获取异常")


if __name__ == '__main__':
    my_score = user_score()
    if my_score >= 1000:
        tecent_jk()
    else:
        print("🦄先别管兑换腾讯月卡了，你还是先攒积分吧......")


