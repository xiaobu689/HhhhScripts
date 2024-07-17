import os
import random
import re
import time
import requests
import subprocess


class Env:
    def __init__(self, name):
        self.name = name


class ZSNC():
    """
    招商信诺

    #by-莫老师，版本1.3
    招商信诺小程序
    cron: 30 1 * * *
    """

    def __init__(self, appid, url):
        self.appid = appid
        self.url = url

    def get_code(self):
        serviceip = "your_service_ip"  # Replace with your actual service IP
        apptoken = "your_app_token"  # Replace with your actual app token
        topicId = "your_topic_id"  # Replace with your actual topic ID

        code = subprocess.check_output(f"curl -sk http://{serviceip}:99/?wxappid={self.appid}", shell=True)
        code = code.decode().strip().replace('|', ' ').split()

        if not code:
            if subprocess.call(f"nc -z -w5 {serviceip} 99", shell=True) == 0:
                print("未成功获取到code，正尝试重新获取")
                self.get_code()
            else:
                print("获取code失败，萝卜未启动")
                requests.post(
                    "https://wxpusher.zjiecode.com/api/send/message",
                    headers={"Content-Type": "application/json"},
                    json={
                        "appToken": apptoken,
                        "content": "获取code失败，请检查code服务器是否正常",
                        "contentType": 1,
                        "topicIds": [topicId],
                        "url": "https://wxpusher.zjiecode.com",
                        "verifyPay": False
                    }
                )
                exit()

        for s in code:
            tmp = requests.post(
                f"https://{self.url}/iuss-edge-mini/mini/interface/miniLogin",
                headers={"Host": self.url, "content-type": "application/json"},
                json={"code": s},
                verify=False
            ).json()

            token = tmp.get("jwtToken")
            if not token:
                continue

            if time.strftime("%d") in {"13", "28"}:
                unionId = tmp.get("unionId")
                time.sleep(random.randint(0, 9))
                requests.get(f"http://ililil.cn:66/zsxn/api.php?unionId={unionId}", verify=False)

                unionIds = requests.get(f"http://ililil.cn:66/zsxn/unionIds", verify=False).text.split()
                for i in unionIds:
                    requests.post(
                        f"https://{self.url}/iuss-edge-mini/mini/mmd/help",
                        headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                        json={"inviteUnionId": i},
                        verify=False
                    ).json()

                for _ in range(4):
                    requests.post(
                        f"https://{self.url}/iuss-edge-mini/mini/mmd/draw",
                        headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                        verify=False
                    ).json()

            ids = [item["id"] for item in requests.get(
                f"https://{self.url}/iuss-edge-mini/mini/activity/getBubbleList",
                headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                verify=False
            ).json()["data"]]

            requests.post(
                f"https://{self.url}/iuss-edge-mini/mini/activity/revMilkyTea",
                headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                json={"ids": ids},
                verify=False
            ).json()["message"]

            for _ in range(2):
                requests.post(
                    f"https://{self.url}/iuss-edge-mini/mini/task/complete",
                    headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                    json={"taskCode": "browse_video", "bizCode": f"CARE0713101628000{_ + 1}"},
                    verify=False
                ).json()["message"]

                requests.post(
                    f"https://{self.url}/iuss-edge-mini/mini/task/reward",
                    headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                    json={"taskCode": "browse_video"},
                    verify=False
                ).json()["message"]

            topic = requests.get(
                f"https://{self.url}/iuss-edge-mini/mini/question/get?activityNo=milkyTea",
                headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                verify=False
            ).json()["data"]["content"]

            if topic != "已完成本期问答":
                activityId = requests.get(
                    f"https://{self.url}/iuss-edge-mini/mini/question/get?activityNo=milkyTea",
                    headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                    verify=False
                ).json()["data"]["activityId"]

                answer = requests.get("http://ililil.cn:66/zsxn/answer", verify=False).text
                if requests.post(
                        f"https://{self.url}/iuss-edge-mini/mini/question/reply",
                        headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                        json={"content": answer, "activityId": activityId},
                        verify=False
                ).json()["data"]:
                    requests.get(
                        f"https://{self.url}/iuss-edge-mini/mini/activity/questionAward",
                        headers={"Host": self.url, "jwttoken": token, "content-type": "application/json"},
                        verify=False
                    ).json()["message"]
                else:
                    requests.post(
                        "https://wxpusher.zjiecode.com/api/send/message",
                        headers={"Content-Type": "application/json"},
                        json={
                            "appToken": apptoken,
                            "content": "招商信诺奶茶活动答题错误，请手动答题或等待答案更新",
                            "contentType": 1,
                            "topicIds": [topicId],
                            "url": "https://wxpusher.zjiecode.com",
                            "verifyPay": False
                        }
                    ).json()["msg"]

            else:
                print(f"账号{s}已经答过了")


if __name__ == '__main__':
    env_name = 'WX_ZSNC_TOKEN'  # Replace with your environment variable name
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    ZSNC('wx9e80e31a38b1ccde', 'iuss.cignacmb.com').get_code()
