# ! /usr/bin/python
# coding=utf-8
import os
import time
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

env_name = 'PZ_CONFIG'
pinzan_config = os.getenv(env_name)
if not pinzan_config:
    print(f'⛔️未获取到配置变量：请检查变量 {env_name} 是否填写')
    exit(0)

# 套餐余量查询
def get_proxies_usage():
    url = 'https://service.ipzan.com/userProduct-get?no=20240524952954587395&userId=7B5L7LBGUS'
    response = requests.get(url)
    if not response or response.status_code != 200:
        print("套餐余量查询失败")
        return
    response_json = response.json()
    balance = response_json["data"]["balance"]
    print(f'🚀代理来源: 品赞代理 | 💰套餐余额: {balance}')

    return balance


# IP提取
def generate_ip(num, minute):
    ip = ''
    ip_api = []
    addWhiteList = False
    params = {
        'num': num,
        'no': pinzan_config['no'],
        'minute': minute,
        'format': 'json',
        'protocol': '1',  # 使用协议：http/https: 1
        'pool': 'quality',  # 优质IP: quality | 普通IP池: ordinary
        'mode': 'auth',  # whitelist: 白名单授权方式 | auth: 账号密码授权
        'secret': pinzan_config['tiqu_secret']
    }
    url = 'https://service.ipzan.com/core-extract'
    response = requests.get(url, params=params)
    if not response or response.status_code != 200:
        print("IP提取失败")
        return ip_api, addWhiteList, ip
    response_json = response.json()
    if response_json["code"] == 0:
        ip_api = response_json["data"]["list"]
        return ip_api, addWhiteList, ip
    else:
        if "加入到白名单再进行提取" in response_json["message"]:
            ip = response_json["message"].split("将")[1].split("加入")[0]
            print(f'⛔️需要将{ip}加入白名单授权后才能进行提取')
            return [], True, ip


# 加入白名单
def white_list_add(ip):
    # 加入白名单
    print('💤开始加入白名单......')

    # 加签的内容
    data = f"{pinzan_config['password']}:{pinzan_config['tiqu_secret']}:{int(time.time())}"
    # 解析签名秘钥，秘钥请在 "控制台" > "控制台"中查看
    key = f"{pinzan_config['sig_secret']}".encode("utf-8")
    # 进行签名
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    # 获得签名好的字符串，在请求添加白名单 API 上传过去即可
    sign = encrypted_data.hex()
    # 添加白名单
    url = "https://service.ipzan.com/whiteList-add"
    payload = {
        "no": pinzan_config['no'],
        "ip": ip,
        "sign": sign,
    }
    response_json = requests.post(url, json=payload).json()

    print(f'🥰{response_json["data"]}')


# 生成代理
def create_proxies(ip_apis):
    api_proxies = []
    for item in ip_apis:
        ip = item["ip"]
        port = item["port"]
        net = item["net"]
        account = item["account"]
        password = item["password"]

        # 代理服务器
        proxyHost = ip
        proxyPort = port

        # 账号密码验证
        proxyMeta = f"http://{account}:{password}@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        print(f'🍄{net} | {ip}:{port}')

        api_proxies.append(proxies)

    return proxies


def pinzan_proxy(num, minute):
    print(f'\n---------------- 代理INFO区域 ----------------')
    print(f'🍳本脚本使用代理 | 提取数量: {num}个 | 有效期: {minute}分钟')
    http_proxies = []
    # 查余额
    balance = get_proxies_usage()
    if balance <= 0:
        print("套餐余额不足")
        return None
    # 提取ip
    ip_apis, addWhiteList, ip = generate_ip(num, minute)
    if ip != "":
        while True:
            # 添加白名单
            white_list_add(ip)
            time.sleep(1)
            # 提取ip
            ip_apis, addWhiteList, ip = generate_ip(num, minute)
            if len(ip_apis) > 0:
                http_proxies = create_proxies(ip_apis)
                break
    elif len(ip_apis) > 0 and addWhiteList == False:
        http_proxies = create_proxies(ip_apis)

    print(f'---------------- 代理INFO区域 ----------------\n')

    return http_proxies


if __name__ == '__main__':
    http_proxies = pinzan_proxy(1, 1)
    print(http_proxies)
