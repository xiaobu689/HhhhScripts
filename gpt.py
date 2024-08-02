from g4f.client import Client

client = Client()


# base
def get_gpt_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content


def ask_choice_question(message):
    message = '''
         问题: 【学条例 守党纪】对于“干预和插手国有企业重组改制、兼并、破产、产权交易、清产核资、资产评估、资产转让、重大项目投资以及其他重大经营活动等事项”的行为，下列说法错误的是____。
         A: 造成不良影响的，给予警告或者严重警告处分
         B: 情节较重的，给予撤销党内职务或者留党察看处分
         C: 情节严重的，给予开除党籍处分
         D: 该行为违反党的廉洁纪律
    '''
    base_desc = "这是一个选择题，请选择出正确答案后直接回答A或B或C或D"
    messages = [{"role": "user", "content": base_desc + message}],
    answer = get_gpt_response(messages)

    return answer


# 示例：提问一个选择题

choice_answer = ask_choice_question("")
print(f"选择题答案：{choice_answer}")