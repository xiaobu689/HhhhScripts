import requests

def login():
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'Hm_lvt_92ae84f463ef5bcfcf04b5b934b6ff8c=1720779538; Hm_lpvt_92ae84f463ef5bcfcf04b5b934b6ff8c=1720779538; HMACCOUNT=99929DF2904D7541; Hm_lvt_b5951e5abc3ca9899bfa1b5a24b96a27=1720779538; Qs_lvt_527572=1720779538; Qs_pv_527572=2979778738696972000; mediav=%7B%22eid%22%3A%221235455%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22f%3AVq%3D.r_)4%3Dt%5B1U1OZ9b%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22f%3AVq%3D.r_)4%3Dt%5B1U1OZ9b%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; _uetsid=26a56100403811ef878381f588757f85; _uetvid=26a57fe0403811ef80c533e80b08f2af; __root_domain_v=.juliangip.com; _qddaz=QD.859920779538329; _qdda=3-1.116z91; _qddab=3-ezqy6f.lyijphhj; lastSE=baidu; Hm_lpvt_b5951e5abc3ca9899bfa1b5a24b96a27=1720779541; _JSID=0f70d9b626f1413f837f204aebcdd073',
        'origin': 'https://www.juliangip.com',
        'priority': 'u=1, i',
        'referer': 'https://www.juliangip.com/user/login',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'type': 'password',
        'username': '17854279565',
        'password': 'Admin201404293',
        'sms_code': '',
    }

    response = requests.post('https://www.juliangip.com/login/go', headers=headers, data=data)
    print(response.text)

def sign():
    print()