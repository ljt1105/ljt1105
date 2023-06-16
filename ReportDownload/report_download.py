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

import SBL_report_download
import trade_report_download


trade_task = trade_report_download.task()
SBL_task = SBL_report_download.task()

schedule.every().day.at("15:36").do(trade_task)
schedule.every().day.at("15:36").do(SBL_task)

while True:
    schedule.run_pending()
    time.sleep(1)

