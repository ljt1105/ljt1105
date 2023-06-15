from pathlib import Path
import os
import win32com.client
import datetime
import re

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

    print("SBL report download complete")

SBL_report_download()