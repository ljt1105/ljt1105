# Import module

from pathlib import Path
import win32com.client
import os

print("Module imported")

# Set attachment saving directory
output_dir = Path("Z:/03.고유/001.Ops/삼성증권 TRS01 거래/07. Test")
print("Set reservoir")

# Making directory when not exist
output_dir.mkdir(parents=True, exist_ok=True)
print("Make folder")

# Accessing outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
print("Access outlook")

# Set mailbox address where attachmnet is
inbox = outlook.GetDefaultFolder(6).Folders("SS-TRS")
print("Access mailbox")

messages = inbox.Items

for message in messages:
    attachments = message.Attachments

    target_folder = output_dir
    target_folder.mkdir(parents=True, exist_ok=True)

    for attachment in attachments:
        attachment.SaveAsFile(target_folder / str(attachment))

print(f'Process finished')

