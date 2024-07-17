"""
北京现代

积分兑换实物，10积分=1元, 车类里面算高的了

抓任意包请求头 token
变量名: BJXD

cron: 25 6 * * *
const $ = new Env("北京现代");
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import save_result_to_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class RUN():
    name = "北京现代"

    def __init__(self, token):
        self.token = token
        self.issue_ids = []
        self.userId = 0
        self.pre_score = 0
        self.headers = {
            'Host': 'bm2-api.bluemembers.com.cn',
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2hpZCI6IjViYmI2Nzg1MTcwZTRlNzRiZmQ3ZTkzM2Q1MjJiMjJjIiwidXNlcl9uYW1lIjoiIiwiZXhwIjoxNzIzOTAyNzI1LCJpc3MiOiJnby5taWNyby5zcnYudXNlciJ9.fOk0IirI7xOiCIbk8oON7t3oNK8_3kxzQU23dFuWaAQ',
            'Accept': '*/*',
            'device': 'iOS',
            'User-Agent': 'ModernCar/8.25.1 (iPhone; iOS 13.4.1; Scale/2.00)',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'App-Version': '8.25.1',
            'Origin-Id': 'DEC39175-978E-4B7B-948F-4176D567831B',
        }

    def user_info(self):
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/account/users/info'
        response_json = requests.get(url, headers=self.headers).json()
        if response_json['code'] == 0:
            nickname = response_json['data']['nickname']
            phone = response_json['data']['phone']
            score_value = response_json['data']['score_value']
            self.pre_score = score_value
            print(f'✅用户信息获取成功 | 用户名: {nickname} | 手机号: {phone} | 积分: {score_value}')

    def user_score_info(self):
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/account/users/info'
        response_json = requests.get(url, headers=self.headers).json()
        if response_json['code'] == 0:
            nickname = response_json['data']['nickname']
            phone = response_json['data']['phone']
            score_value = response_json['data']['score_value']
            self.pre_score = score_value
            diff_score = score_value - self.pre_score
            print(f'✅用户: {phone} | 总积分: {score_value} |今日新增积分: {diff_score}')

    def sign(self):
        score = ''
        hid = ''
        # 签到抽奖
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/user/reward_list'
        response_json = requests.get(url, headers=self.headers).json()
        print(response_json)
        if response_json['code'] == 0:
            hid = response_json['data']['hid']
            list = response_json['data']['list']
            for item in list:
                if item["hid"] == hid:
                    score = item["score"]
                    print(f'✅如果签到成功 | 积分+{score}')

        # 状态上报
        json_data = {
            'hid': hid,
            'hash': '1e50985eb492d46dffe1fb910db20dd1',  # 32位，大概率MD5小写，用CC_MD5 hook
            'sm_deviceId': '',
            'ctu_token': None,
        }
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/user/reward_report'
        response_json_ = requests.post(url, headers=self.headers, json=json_data).json()
        print(response_json_)
        if response_json_['code'] == 0:
            print(f'✅签到成功 | 积分+{score}')
        else:
            print(f'❌签到失败， {response_json_["message"]}')

    # 浏览3篇文章5积分
    def view_article(self):
        article_ids = [
            "bc16823d560342b4bb3b88dea31f4b3a",
            "ff6ebcc06fbc4416a14ee0ef28f97b3c",
            "25c627e605714e948f65c4c12c97b1c3"
        ]
        article_id = random.choice(article_ids)
        print(f'✅浏览文章 | 文章ID: {article_id}')
        url = f'https://bm2-api.bluemembers.com.cn/v1/app/white/article/detail_app/{article_id}'
        response = requests.get(url, headers=self.headers)
        print(response.text)

    def article_score_add(self):
        '''
        ctu_token 的长度非常长，且包含了很多字母、数字、特殊字符（如 - 和 _），这表明它可能是经过多次编码或加密的结果。
        这种长度和混合字符的特征常见于 Base64 编码后的加密数据。
        ----------------------------------------------
        常见加密算法：
        对称加密：如果使用对称加密（如 AES），通常会对数据进行加密，然后再进行 Base64 编码，以便在 URL 或 JSON 中传递。
        非对称加密：非对称加密（如 RSA）通常用于加密密钥或敏感数据。
        哈希算法：不太可能，因为哈希函数（如 SHA-256）生成的长度固定，且没有解密过程。
        ----------------------------------------------
        可能的加密类型：基于 ctu_token 的长度和混合字符特征，它很可能是经过对称加密（如 AES）并进行 Base64 编码的结果。
        验证方法：使用静态和动态分析工具（如 Frida）拦截和记录加密函数调用，获取加密前的原始数据。
        '''

        json_data = {
            'ctu_token': 'dtNaeNjOUKohjTjtXdBQFfkwUjGgzWZbFtskg6ernJiRZF1W4jCvOoBEU3iKR8x-cKnXsUweHhi0ipIDgpbaIdJJaQIBzJ9ZSdw32tt3rLmfY7y9Ftx3mGcHPYpQyCzUZDu6efMK1H5-Fh3FMsr2HS4ZgcJxZj0asxvi-G_cxufMVe0NcmfWfEeRCF0kJhCzQTL_HkoBX9sLdlI6BDf7esnszXleoCwu47AovTREgmB3hiy9QX3bZavwdfhv2AB_UFBtMtkEaSLs0VsWfsIfFceNz_b6NONNHoveJo9TZ4oWPpjIDz8dDPP2o3qaWxj7otPFbV0_SBdaQGfjWPKDRN_ZclV241PAzmz1njhE087AFjSxRC9uWvfnraKfTN--ulHxIR7mu7pRYV4GuO3DnncrWdViXEa-NhVHM10sHbH3r2_gZEbINYR2rWWEMW6y2mw3PmnLCIdflnehwSzW4Rsv2dIXzyy3TZxCFPP_qc03hXxstnQZZ9vc1WtKueOhn4CbzZtUH5n-Fiywirq7CdlJiVvq2mL3ZD6Wf9IX8XlHYOq0CZ_H4j0oYhNnsH0G5CkCBBNlxWHCPOsrk80vxkLXDw5zvSO2UphR0xBa7z6e4PYKa0iEHLle1d4sS8FFjGFvAfsprcgrHpimhvVL89Dwe-Yy2SzaW-hinkmCKfKT_sv_NuNSI2GiLo-0n54-_FLc4ddtxRWYdU_7Tr-YctT7juDEb6o8kepKCYLefK2IcYtzCnSGl8d4Mb4SalW-eVzAJDHgdYHjOt81c1h3MEIkySjpWxQ4kzKNRdSYGrBAzL6SBM-q479f_qmPVxc3DCwS6F6XcC3w9TV9Y1XDA3L5TJ53EHsGql6zZiqj2ISl7Wdn7ugA6EsgAtZRygtUhYDPosIGmOG7wnJJhRaz2tAveAXjQBj0gVuiDVtdpjCKYYjmw7sS6RkmfkCkh_zxtRsD4AuAvUvoDXgOgs7Th4k3FdOOiUbUwW0g6MRoaaHKbmyKhUJ6WDuzxmO7BMZVjLWJKQRz7ubIwP5A5776AzQt7xRwkWkiCiVV2DNUTRdN69ixx1fhldM9NbYLh-XrX-N6JL-0_Wbt62WTsUVwBbP5y2PtHgZAu3fK8Vdmt6U9x2-uwU__Vkto8CacXQGVHA4cP1dKaTyH6ee5A4uohQgdF3nGRnF-FLETBRK22B7U9QDbif1-baWmNLl6NOBFGSEqXLMvHovVkyFOgdCVcbFNhN087HjM5MC74PrnNdJx5fSkl_sEE81OmOLqWQHcxVHhM50wD9ex1lyiwderFQTvMk2uDEuo4xyTFwMyQ9GlUjhsKKiqMzCg-8nHeTclsbWs4T62ThwwyF826xOKsvGE1b8k1gspqBNa6WiURPY-0w1g3PJBIlqmd872Vrqz3Hzw-zwFVkUCiLGAr97M6Op1Tqjia-SBTCDt0LW6Uta5l8yrsHkTT2bu7lAcuL_4H6BtNg3EgXJUoum84EkT4VhltKf4sxqm0cTu5F9dnLauzHZJ1eoU8D9zS6JPQUjj!8c8b64324274bd85cb1a410769046ca5!03afaaf9bcad2e4b81bb571b58135aa3!v6.1.4r.578bf7d1',
            'action': 12,
        }
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/score'
        response_json_ = requests.post(url, headers=self.headers, json=json_data).json()
        if response_json_['code'] == 0:
            score = response_json_['data']['score']
            print(f'✅浏览文章成功 | 积分+{score}')

    # 每日问答
    def daily_question(self):
        params = {
            'date': '20240714',
        }
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/special/daily/ask_info'
        response_json = requests.get(url, params=params, headers=self.headers).json()
        if response_json['code'] == 0:
            question_info = response_json['data']['question_info']
            questions_hid = question_info['questions_hid']
            # 题目
            content = question_info['content']
            print(content)
            # 选项
            options = question_info['option']
            for option in options:
                option_content = option['option_content']
                print(f'{option["option"]}. {option_content}')
            return questions_hid

    def answer_question(self, questions_hid, answer):
        json_data = {
            'answer': 'A',
            'questions_hid': questions_hid,
            'ctu_token': 'dtNaeNjOUKohjTjtXdBQFfkwUjGgzWZbFtskg6ernJiRZF1W4jCvOoBEU3iKR8x-cKnXsUweHhi0ipIDgpbaIdJJaQIBzJ9ZSdw32tt3rLmfY7y9Ftx3mGcHPYpQyCzUZDu6efMK1H5-Fh3FMsr2HS4ZgcJxZj0asxvi-G_cxufMVe0NcmfWfEeRCF0kJhCzQTL_HkoBX9sLdlI6BDf7esnszXleoCwu47AovTREgmB3hiy9QX3bZavwdfhv2AB_UFBtMtkEaSLs0VsWfsIfFceNz_b6NONNHoveJo9TZ4oWPpjIDz8dDPP2o3qaWxj7otPFbV0_SBdaQGfjWPKDRN_ZclV241PAzmz1njhE087AFjSxRC9uWvfnraKfTN--ulHxIR7mu7pRYV4GuO3DnncrWdViXEa-NhVHM10sHbH3r2_gZEbINYR2rWWEMW6y2mw3PmnLCIdflnehwSzW4Rsv2dIXzyy3TZxCFPP_qc03hXxstnQZZ9vc1WtKueOhn4CbzZtUH5n-Fiywirq7CdlJiVvq2mL3ZD6Wf9IX8XlHYOq0CZ_H4j0oYhNnsH0G5CkCBBNlxWHCPOsrk80vxkLXDw5zvSO2UphR0xBa7z6e4PYKa0iEHLle1d4sS8FFjGFvAfsprcgrHpimhvVL89Dwe-Yy2SzaW-hinkmCKfKT_sv_NuNSI2GiLo-0n54-_FLc4ddtxRWYdU_7Tr-YctT7juDEb6o8kepKCYLefK2IcYtzCnSGl8d4Mb4SalW-eVzAJDHgdYHjOt81c1h3MEIkySjpWxQ4kzKNRdSYGrBAzL6SBM-q479f_qmPVxc3DCwS6F6XcC3w9TV9Y1XDA3L5TJ53EHsGql6zZiqj2ISl7Wdn7ugA6EsgAtZRygtUhYDPosIGmOG7wnJJhRaz2tAveAXjQBj0gVuiDVtdpjCKYYjmw7sS6RkmfkCkh_zxtRsD4AuAvUvoDXgOgs7Th4k3FdOOiUbUwW0g6MRoaaHKbmyKhUJ6WDuzxmO7BMZVjLWJKQRz7ubIwP5A5776AzQt7xRwkWkiCiVV2DNUTRdN69ixx1fhldM9NbYLh-XrX-N6JL-0_Wbt62WTsUVwBbP5y2PtHgZAu3fK8Vdmt6U9x2-uwU__Vkto8CacXQGVHA4cP1dKaTyH6ee5A4uohQgdF3nGRnF-FLETBRK22B7U9QDbif1-baWmNLl6NOBFGSEqXLMvHovVkyFOgdCVcbFNhN087HjM5MC74PrnNdJx5fSkl_sEE81OmOLqWQHcxVHhM50wD9ex1lyiwderFQTvMk2uDEuo4xyTFwMyQ9GlUjhsKKiqMzCg-8nHeTclsbWs4T62ThwwyF826xOKsvGE1b8k1gspqBNa6WiURPY-0w1g3PJBIlqmd872Vrqz3Hzw-zwFVkUCiLGAr97M6Op1Tqjia-SBTCDt0LW6Uta5l8yrsHkTT2bu7lAcuL_4H6BtNg3EgXJUoum84EkT4VhltKf4sxqm0cTu5F9dnLauzHZJ1eoU8D9zS6JPQUjj!8c8b64324274bd85cb1a410769046ca5!03afaaf9bcad2e4b81bb571b58135aa3!v6.1.4r.578bf7d1',
        }
        url = 'https://bm2-api.bluemembers.com.cn/v1/app/special/daily/ask_answer'
        response_json = requests.post(url, headers=self.headers, json=json_data).json()
        if response_json['code'] == 0:
            answer = response_json['data']['answer']  # C.造价低
            score = response_json['data']['answer_score']
            if answer.split('.')[0] == answer:
                print(f'✅恭喜你回答正确 | 积分+{score}')
            else:
                print(f'❌恭喜你回答错误 | 积分+{score}')

    # 邀请好友答题
    def recommend_answer(self):
        data = {
            'category': '101',
            'data_hid': 'e48115f4c31044b6b34063d5787e31ae',
        }
        response_json = requests.post(
            'https://bm2-api.bluemembers.com.cn/v1/app/white/common/recommend', headers=self.headers, data=data).json()
        if response_json['code'] == 0:
            '''
            "title": "大神帮我，这道题太难了！",
		    "pic": "https://bm2-res.bluemembers.com.cn/res/static/logo.jpg",
		    "qr_code": "",
		    "url": "https://bm2-wx.bluemembers.com.cn/browser/day-question?share_user_hid=5bbb6785170e4e74bfd7e933d522b22c\u0026hid=e48115f4c31044b6b34063d5787e31ae\u0026date=20240713\u0026topage=dayQuestion",
		    "mini_pro_url": "",
		    "desc": "答对可获5积分~",
		    "fine_level": 0,
		    "status_name": "",
		    "mini_id": "gh_4967ce20bc32",
		    "mini_type": "0"
            '''
            url = response_json['data']['url']

    def main(self):
        self.user_info()
        self.sign()
        # for i in range(3):
        #     self.view_article()
        #     time.sleep(random.randint(10, 15))
        # self.article_score_add()
        # exit(0)
        # questions_hid = self.daily_question()
        # self.answer_question(questions_hid, 'A')


if __name__ == '__main__':
    env_name = 'BJXD'
    tokenStr = os.getenv(env_name)
    tokenStr = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2hpZCI6IjViYmI2Nzg1MTcwZTRlNzRiZmQ3ZTkzM2Q1MjJiMjJjIiwidXNlcl9uYW1lIjoiIiwiZXhwIjoxNzIzOTAyNzI1LCJpc3MiOiJnby5taWNyby5zcnYudXNlciJ9.fOk0IirI7xOiCIbk8oON7t3oNK8_3kxzQU23dFuWaAQ'
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"北京现代共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        RUN(token).main()
        print("\n随机等待30-60s进行下一个账号")
        time.sleep(random.randint(30, 60))
