# Import module

from pathlib import Path
import win32com.client
import os

def margin_report_download():
    # Set attachment saving directory
    output_dir = Path("Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test")

    # Making directory when not exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Accessing outlook
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # Set mailbox address where attachmnet is
    inbox = outlook.GetDefaultFolder(6).Folders("SS-MR")


    messages = inbox.Items

    for message in messages:
        if message.Unread:

            attachments = message.Attachments

            target_folder = output_dir
            target_folder.mkdir(parents=True, exist_ok=True)

            for attachment in attachments:
                attachment.SaveAsFile(target_folder / str(attachment))
                
                if message.Unread:
                    message.Unread = False

    print(f'MarginReport download completed')