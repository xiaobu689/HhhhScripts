from openai import OpenAI

client = OpenAI(
    api_key="sk-X9Gcqj7Wy0HIlZvkWoWmNo5GXV6Zx1lO0u8CSUxNGhFGzheJ",
    base_url="https://api.chatanywhere.tech/v1"
)

choice_base_desc = "这是一个选择题，请选择出正确答案后直接回答A或B或C或D，严格按照以下格式回答：芝麻开门#你的答案#芝麻开门\n"
comment_base_desc = "这是一个文章评论"


# 非流式响应
def gpt_35_api(message):
    """为提供的对话消息创建新的回答

    Args:
        message: 消息文本
    """
    messages = [{'role': 'user','content': choice_base_desc+message},]
    print("----------messages=", messages)
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

if __name__ == '__main__':

    message = '''
Q：前行时发生车辆/行人碰撞危险，哪个系统可以进行紧急制动（）
A: FCA
B: FCW
C: RCCA
D: DAW
    '''
    # 非流式调用
    gpt_35_api(message)
    # 流式调用
    # gpt_35_api_stream(messages)