"""
艺龙旅行

抓任意包请求头 TC-MALL-USER-TOKEN
变量名: YL_TOKEN

cron: 27 7 * * *
const $ = new Env("艺龙旅行");
"""
import os
import random
import re
import time
from common import save_result_to_file
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class YL():
    name = "艺龙旅行"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Host': 'wx.17u.cn',
            #'Cookie': 'saviorInfo={"platid":"10056","chid":"ewiphone","tc_deviceid":"FAB59F1D-8D2F-4CAA-82EF-4B23460FA23F","ecrd":"","v":"10.5.3","el_deviceid":"FAB59F1D-8D2F-4CAA-82EF-4B23460FA23F","refid":"1899509596","memberid":"51UjeGypMuo8FImDeF7UYya6L_OzZsautkZqNevPCNNsNtpUVC0pL7bdrPHQ0TLGxjiSlCWWsCM6p0-XU93RUV5bmfBDmbswkZlx2IQENvRI2UpTo8qOrLo2C0jHqZKjfYm4IF7FciCpzxLeA5QJV4ow**"}',
            'TC-MALL-USER-TOKEN': '51UjeGypMuo8FImDeF7UYya6L_OzZsautkZqNevPCNNsNtpUVC0pL7bdrPHQ0TLGxjiSlCWWsCM6p0-XU93RUV5bmfBDmbswkZlx2IQENvRI2UpTo8qOrLo2C0jHqZKjfYm4IF7FciCpzxLeA5QJV4ow**',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 TcTravel/10.5.3 ElTravel tctype/wk',
            'TC-MALL-PLATFORM-SUB': 'EAPP',
            'Referer': 'https://wx.17u.cn/mileagemall/activity/mallVue3/home?showBack=1&refid=1935010948',
            'TC-MALL-PLATFORM-CODE': 'EAPP',
            'TC-MALL-DEPT-CODE': 'iH3PGf9ZucSMMEYi4keylA==',
            'TC-MALL-CLIENT': 'API_CLIENT',
            'Origin': 'https://wx.17u.cn',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Site': 'same-origin',
            'TC-MALL-OS-TYPE': 'IOS',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Sec-Fetch-Mode': 'cors',
        }
    def sign(self):
        json_data = {}
        url = 'https://wx.17u.cn/wxmpsign/sign/saveSignInfo'
        response = requests.post(url, headers=self.headers, json=json_data)
        if not response or response.status_code != 200:
            save_result_to_file("success", self.name)
            print("签到异常：", response.text)
            return
        response_json = response.json()
        if response_json['code'] == 200:
            save_result_to_file("success", self.name)
            signMileage = response_json['data']['signMileage']
            totalIncome = response_json['data']['totalIncome']
            periodContinuedSignDays = response_json['data']['periodContinuedSignDays']
            brokenSign = response_json['data']['brokenSign']
            print(f'✅签到成功 | 💰签到获得{signMileage}积分 | 🐶连续签到{periodContinuedSignDays}天')
        elif response_json['code'] == 500:
            save_result_to_file("success", self.name)
            print(f'✅签到成功 | {response_json["msg"]}')
        else:
            save_result_to_file("success", self.name)
            print(f'❌签到失败：{response_json["msg"]}')

    def main(self):
        self.sign()


if __name__ == '__main__':
    env_name = 'YL_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"艺龙旅行共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        YL(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
        print("----------------------------------")
