"""
星空代理签到

注册地址: https://www.xkdaili.com/?ic=8wcz5adz
变量名: xingkong
格式： phone#password
cron: 35 6 * * *
const $ = new Env("星空代理签到");
"""

import json
import os
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


def xingkong(phone, password):
    print(f'开始帐号签到......')
    url = 'https://www.xkdaili.com/tools/submit_ajax.ashx?action=user_login&site_id=1'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '50',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.xkdaili.com',
        'Origin': 'https://www.xkdaili.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://www.xkdaili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'username': phone,
        'password': password,
        'remember': 1
    }
    response = requests.post(url=url, headers=headers, data=data, verify=False)
    cookie = str(requests.utils.dict_from_cookiejar(response.cookies)).replace(',', ';').replace(':', '=').replace('\'',
                                                                                                                   '').replace(
        '{', '').replace('}', '').replace(' ', '')
    r = json.loads(response.text)['msg']
    print(f'{r}')

    url_sign = 'https://www.xkdaili.com/tools/submit_ajax.ashx?action=user_receive_point'
    headers_sign = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '10',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'Host': 'www.xkdaili.com',
        'Origin': 'https://www.xkdaili.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://www.xkdaili.com/main/usercenter.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data_sign = {
        'type': 'login'
    }
    html_sign = requests.post(url=url_sign, headers=headers_sign, data=data_sign, verify=False)
    result = json.loads(html_sign.text)['msg']
    print(f'✅{r} | 获得: {result["point"]}星币')


if __name__ == '__main__':
    env_name = 'xingkong'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    phone = tokenStr.split('#')[0]
    password = tokenStr.split('#')[1]
    xingkong(phone, password)
