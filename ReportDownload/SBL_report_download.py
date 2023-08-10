import sys
sys.path.append(r'C:/PythonProjects/ljt1105/ReportDownload')

from pathlib import Path
import os
import win32com.client
import datetime
import re
import trade_report_download
import schedule
import time

def SBL_report_download():
    output_dir = Path("Z:/02.펀드/007.대차거래(보관의무)")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6).Folders("DIRECTIONAL")
    messages = inbox.Items

    for message in messages:
        if message.Unread:
            subject = re.sub(r'[:<>]', '_', message.Subject) 
            received_date = message.ReceivedTime
            timestamp = received_date.strftime("%Y%m%d_%H%M%S")
            new_subject = f"{subject}_{timestamp}"

            message.SaveAs(output_dir / f"{new_subject}.msg")
            message.Unread = False

    print("SBL report download completed")


SBL_report_download()

# def task():
#     today = datetime.datetime.now().date()
#     # 주말인 경우에는 실행하지 않음
#     if today.weekday() >= 5:
#         return
#     # 평일인 경우에만 특정 시간에 실행
#     if today.weekday() <= 4:
#         current_time = datetime.datetime.now().time()
#         target_time = datetime.time(16, 30, 0) # 실행할 특정 시간 설정(16시 30분)
#         if current_time >= target_time:
#             SBL_report_download()

# schedule.every().day.at("16:30").do(task)

# while True:
#     schedule.run_pending()
#     time.sleep(1)