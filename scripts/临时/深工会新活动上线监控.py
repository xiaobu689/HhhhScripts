"""
深工会新活动上线监控

没啥用，监控新活动用的

cron: */5 * * * *
const $ = new Env("深工会新活动上线监控");
"""

import requests

from sendNotify import send

pkAdTags = []


def get_hds():
    global pkAdTags
    headers = {
        'Host': 'lsapp.szzgh.org:99',
        'Connection': 'keep-alive',
        'token': '',
        'content-type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x1800323d) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxb7a23c5650537af6/275/page-frame.html',
    }

    response = requests.get('https://lsapp.szzgh.org:99/api/ebs/hd/ad/getIndexAdInfo', headers=headers)
    response_json = response.json()
    if response_json['code'] == 0:
        list = response_json['data']
        if len(pkAdTags) == 0:
            pkAdTags = [item['pkAdTag'] for item in list]
        else:
            content = ''
            for item in list:
                title = item['title']
                pkAdTag = item['pkAdTag']
                adList = item['adList']
                if pkAdTag not in pkAdTags:
                    content += f'{title}\n'
                    if len(adList) > 0:
                        if 'putStartTime' in adList[0]:
                            content += f'活动时间: {adList[0]["putStartTime"]} - {adList[0]["putEndTime"]}\n'
                    print('有新活动上线')
                    send('深工会新活动通知', content)


if __name__ == '__main__':
    get_hds()
