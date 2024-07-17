

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


def user_score():
    response = requests.get('https://cmallapi.haday.cn/buyer-api/members/points/current', headers=headers)
    if not response or response.status_code != 200:
        print("获取积分失败")
        return
    response_json = response.json()
    print(f'🐍积分：{response_json["consum_point"]}')

    return response_json["consum_point"]

def goods_list():
    can_exchange = []
    my_score = user_score()
    if not my_score:
        print("积分异常")
        return
    params = {
        'sort': 'synthesis_desc',
        'tag_code': '',
        'page_no': '1',
        'total': '90',
        'page_size': '90',
    }
    response = requests.get('https://cmallapi.haday.cn/buyer-api/point/goods/list', params=params, headers=headers)
    if not response or response.status_code != 200:
        print("获取商品列表失败")
        return
    response_json = response.json()
    list = response_json["data"]
    for item in list:
        goods_id = item["goods_id"]
        goods_name = item["goods_name"]
        need_point = item["need_point"]
        enable_quantity = item["enable_quantity"]
        msg = f'🐍{goods_id} | {goods_name} | {need_point} | {enable_quantity}'
        print(msg)
        if my_score >= need_point and enable_quantity > 0:
            msg = f'🐍{goods_id} | {goods_name} | {need_point} | {enable_quantity}'
            print(msg)
            can_exchange.append(msg)

    return can_exchange


if __name__ == '__main__':
    goods_list()