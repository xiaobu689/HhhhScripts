import requests

def goods_list():
    headers = {
        'Host': 'zm.t7a.cn',
        'Connection': 'keep-alive',
        'content-type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003137) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx94dca6ef07a54c55/150/page-frame.html',
    }
    params = {
        'safe': '啥也不是',
        'type': '1',
    }

    response = requests.get('https://zm.t7a.cn/api/getgoodlists.php', params=params, headers=headers)
    print(response.text)
    response_json = response.json()
    if response_json['status'] == 1:
        for item in response_json['data']:
            id = item['id']
            name = item['title']
            score = item['score']
            monthcount = item['monthcount']
            monthexnum = item['monthexnum']

if __name__ == '__main__':
    # 商品列表
    goods_list()