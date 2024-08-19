
import requests
from json import dumps as jsonDumps


# 青龙API类
class QL:
    def __init__(self, address: str, id: str, secret: str) -> None:
        self.address = address
        self.id = id
        self.secret = secret
        self.valid = True
        self.login()

    def log(self, content: str) -> None:
        print(content)

    def login(self) -> bool:
        url = f"{self.address}/open/auth/token?client_id={self.id}&client_secret={self.secret}"
        try:
            rjson = requests.get(url).json()
            if rjson['code'] == 200:
                self.auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
                return True
            else:
                self.log(f"登录失败：{rjson['message']}")
        except Exception as e:
            self.valid = False
            self.log(f"登录失败：{str(e)}")
        return False

    def getEnvs(self) -> (bool, list):
        url = f"{self.address}/open/envs?searchValue="
        headers = {"Authorization": self.auth}
        try:
            rjson = requests.get(url, headers=headers).json()
            if rjson['code'] == 200:
                return True, rjson['data']
            else:
                self.log(f"获取环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"获取环境变量失败：{str(e)}")
        return False, []

    def getEnvsByName(self, keyword: str) -> (bool, list):
        if keyword == '':
            url = f"{self.address}/open/envs?searchValue="
        else:
            url = f"{self.address}/open/envs?searchValue={keyword}"
        headers = {"Authorization": self.auth}
        try:
            rjson = requests.get(url, headers=headers).json()
            if rjson['code'] == 200:
                return True, rjson['data']
            else:
                self.log(f"获取环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"获取环境变量失败：{str(e)}")
        return False, []

    def deleteEnvs(self, ids: list) -> bool:
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth, "content-type": "application/json"}
        try:
            rjson = requests.delete(url, headers=headers, data=jsonDumps(ids)).json()
            if rjson['code'] == 200:
                self.log(f"删除环境变量成功：{len(ids)}")
                return True
            else:
                self.log(f"删除环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"删除环境变量失败：{str(e)}")
        return False

    def addEnvs(self, envs: list) -> bool:
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth, "content-type": "application/json"}
        try:
            rjson = requests.post(url, headers=headers, data=jsonDumps(envs)).json()
            if rjson['code'] == 200:
                self.log(f"新建环境变量成功：{len(envs)}")
                return True
            else:
                self.log(f"新建环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"新建环境变量失败：{str(e)}")
        return False

    def updateEnv(self, env: dict) -> bool:
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth, "content-type": "application/json"}
        try:
            rjson = requests.put(url, headers=headers, data=jsonDumps(env)).json()
            if rjson['code'] == 200:
                self.log(f"更新环境变量成功")
                return True
            else:
                self.log(f"更新环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"更新环境变量失败：{str(e)}")
        return False