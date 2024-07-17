"""
CK测活通知

cron: 20 7,12,18 * * *
const $ = new Env("CK测活通知");
"""

import os
from datetime import datetime
from sendNotify import send


# 读取结果并通知
def read_and_notify():
    # 获取当前日期并格式化
    today_date = datetime.now().strftime("%Y%m%d")
    file_name = f'script_results_{today_date}.txt'
    try:
        # 删除旧数据
        files = os.listdir('.')
        # 筛选出包含 'script_results' 但不是今天的文件
        files_to_delete = [f for f in files if 'script_results' in f and today_date not in f]
        # 删除这些文件
        for f in files_to_delete:
            os.remove(f)

        # 读取新数据
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        total_scripts = len(lines)
        success_count = sum(1 for line in lines if '✅' in line)
        failure_count = sum(1 for line in lines if '❌' in line)
        summary = f"总脚本数 {total_scripts}，成功 {success_count}，失败 {failure_count} 个。\n\n"
        # 筛选出失败的结果和汇总信息
        failure_lines = [line for line in lines if '❌' in line]
        notification_message = summary + "\n".join(failure_lines)  # 将汇总信息和失败的结果拼接为通知内容

        # 发送通知
        send("脚本执行结果汇总", notification_message)
    except Exception as e:
        print(f"读取文件或发送通知时出现异常：{str(e)}")


if __name__ == '__main__':
    read_and_notify()
