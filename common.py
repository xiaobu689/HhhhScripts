from datetime import datetime
import json
import requests
import random
import re
import time
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

# import os
# from http import HTTPStatus
# import dashscope


# 通义千问API
def qianwen_messages(basic_question, question):
    content = ''
    # qw_key = os.getenv("QIANWEN_KEY")
    # if not qw_key:
    #     print(f'⛔️未获取到通义千问key：请检查变量 {qw_key} 是否填写')
    # else:
    #     dashscope.api_key = qw_key
    #     messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
    #                 {'role': 'user', 'content': basic_question + question}]
    #     response = dashscope.Generation.call(
    #         dashscope.Generation.Models.qwen_turbo,
    #         messages=messages,
    #         seed=random.randint(1, 10000),
    #         result_format='message',
    #     )
    #     if response.status_code == HTTPStatus.OK:
    #         content = response['output']['choices'][0]['message']['content']
    #     else:
    #         print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
    #             response.request_id, response.status_code,
    #             response.code, response.message
    #         ))
    return content


def make_request(url, json_data=None, method='get', headers=None):
    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, verify=False)
        else:
            response = requests.post(url, headers=headers, json=json_data, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # 这里可以处理错误，例如记录日志或设置全局变量
        print(f"请求错误: {e}")
        return None


def get_current_timestamp_milliseconds():
    # 获取当前时间
    current_time = datetime.now()
    # 将当前时间转换为时间戳（秒级）
    timestamp_seconds = int(time.mktime(current_time.timetuple()))
    # 将秒级时间戳转换为毫秒级
    timestamp_milliseconds = timestamp_seconds * 1000 + current_time.microsecond // 1000
    return timestamp_milliseconds


def daily_one_word():
    urls = [
        "https://api.xygeng.cn/openapi/one",
        "https://v1.hitokoto.cn",
    ]
    url = random.choice(urls)
    response = requests.get(url, verify=False)
    if response and response.status_code == 200:
        response_json = response.json()
        if url == "https://api.xygeng.cn/openapi/one":
            return response_json['data']['content']
        elif url == "https://v1.hitokoto.cn":
            return response_json['hitokoto']
        else:
            return None
    else:
        return None


# 随机一句网易云热评
def get_163music_comments():
    comments = []
    keywords_to_filter = ['苏苏', '这首', '歌', '听', '发行', '编曲', '曲', '唱', '生日快乐', '生日', '中考',
                          '高考', '加油', '小猫', '西子', '好听', '音乐',
                          ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    }

    ids = [3778678, 6723173524, 5059661515]
    id = random.choice(ids)
    url = f'https://music.163.com/discover/toplist?id={id}'  # 热歌榜的url
    response = requests.get(url, headers=headers)
    music_ids = re.findall('<a href="/song\?id=(\d+)"', response.text)
    music_id = random.choice(music_ids)
    get_url = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + music_id + "?limit=0&offset=0"
    response = requests.get(get_url, headers=headers)

    json_dict = json.loads(response.content.decode("utf-8"))
    hotcomments = json_dict["hotComments"]
    for j in hotcomments:
        content = j["content"].replace("\n", " ")
        nickname = j["user"]["nickname"]
        liked = str(j["likedCount"]) + "赞"
        # print(f"{nickname} | {content} | {liked}赞")

        # 过滤带有数字的句子
        if any(char.isdigit() for char in content):
            print("包含数字，跳过")
            continue

        # 过滤特殊表情符号和书名号《》
        if re.search(r'[《》]', content):
            print("包含特殊符号，跳过")
            continue

        # 检查评论中是否包含任何关键词
        if any(keyword in content for keyword in keywords_to_filter):
            print("包含关键词，跳过")
            continue
        if len(content) <= 40:
            continue
        # 定义一个正则表达式模式，用于匹配表情符号
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F"
            "\U0001F780-\U0001F7FF"
            "\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002702-\U000027B0"
            "]+",
            flags=re.UNICODE,
        )
        # 定义一个正则表达式模式，用于匹配特殊字符
        special_char_pattern = re.compile(r'[^\w\s，。！？、‘’“”（）【】《》]+')
        # 替换表情符号
        hot_comment = emoji_pattern.sub(r'', content)
        # 使用正则表达式替换特殊字符为空字符串
        clean_text = special_char_pattern.sub('', hot_comment)
        comments.append(clean_text)

    if len(comments) > 0:
        return random.choice(comments)
    else:
        return None


# 获取代理IP
def get_ip():
    response = requests.get('https://cdn.jsdelivr.net/gh/parserpp/ip_ports/proxyinfo.json', verify=False)
    # 使用正则表达式提取 IP 地址和端口号
    data = response.text
    lines = data.strip().split('\n')
    json_objects = [json.loads(line) for line in lines if json.loads(line)["country"] == "CN"]
    if json_objects:
        selected = random.choice(json_objects)
        result = f"{selected['type']}://{selected['host']}:{selected['port']}"

        proxies = {
            selected['type']: result,
        }
        print(f"当前代理：{result}")
        return proxies
    else:
        print("没匹配到CN的ip")
        return None


# 保存结果到文件
def save_result_to_file(status, name):
    if status == "success":
        result = f'✅【{name}】 | CK正常'
    elif status == "error":
        result = f'❌【{name}】 | CK已失效'

    # 获取当前日期并格式化
    today_date = datetime.now().strftime("%Y%m%d")
    file_name = f'script_results_{today_date}.txt'

    try:
        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(f'{result}\n')
    except Exception as e:
        print(f"保存结果到文件时出现异常：{str(e)}")


def random_delay(min_delay=1, max_delay=5):
    """
    在min_delay和max_delay之间产生一个随机的延时时间，然后暂停执行。
    参数:
    min_delay (int/float): 最小延时时间（秒）
    max_delay (int/float): 最大延时时间（秒）
    """
    delay = random.uniform(min_delay, max_delay)
    print(f">本次随机延迟：【{delay:.2f}】 秒.....")
    time.sleep(delay)


# if __name__ == '__main__':
#     word = daily_one_word()
#     print(word)
