import os

from openai import OpenAI

env_name = "GPT"
gpt_config = os.getenv(env_name)
url, key = gpt_config.split('#')

if url == "" or key == "":
    print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
    exit(0)

client = OpenAI(
    api_key=key,
    base_url=url
)

choice_base_desc = "这是一个选择题，请选择出正确答案后直接回答A或B或C或D，严格按照以下格式回答：芝麻开门#你的答案#芝麻开门\n"
comment_base_desc = ""


# 非流式响应
def gpt_35_api(message):
    """为提供的对话消息创建新的回答

    Args:
        message: 消息文本
    """
    messages = [{'role': 'user','content': message},]
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)

# 选择题GPT
def gpt_35_api_choice(message):
    """为提供的对话消息创建新的回答

    Args:
        message: 消息文本
    """
    messages = [{'role': 'user','content': choice_base_desc+message},]
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)

# 评论GPT
def gpt_35_api_comment(message):
    """为提供的对话消息创建新的回答

    Args:
        message: 消息文本
    """
    messages = [{'role': 'user','content': comment_base_desc+message},]
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)

# 流式响应
def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

# if __name__ == '__main__':
#     # 非流式调用
#     gpt_35_api(message)
#     # 流式调用
#     # gpt_35_api_stream(messages)