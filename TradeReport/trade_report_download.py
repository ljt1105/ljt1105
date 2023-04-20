from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path
import os
import win32com.client


def kb_pbs_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/KB")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("KB-PBS")
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

    print("KB-PBS Trade report download complete")


def nh_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/NH")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("NH")
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

    print("NH Trade report download complete")


def kis_pbs_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/KIS-PBS")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("KIS-PBS")
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

    print("KIS-PBS Trade report download complete")

def kis_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/KIS")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("KIS")
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

    print("KIS Trade report download complete")


def yuanta_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/Yuanta")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("Yuanta")
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

    print("Yuanta Trade report download complete")


def miraeasset_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/MiraeAsset")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("MiraeAsset")
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

    print("MiraeAsset Trade report download complete")


def hsbc_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/HSBC")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("HSBC")
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

    print("HSBC Trade report download complete")


# def trade_report_download():
if __name__ == "__main__":
    print("===================================================")
    kb_pbs_trade_report_download()
    print("===================================================")
    nh_trade_report_download()
    print("===================================================")
    kis_pbs_trade_report_download()
    print("===================================================")
    kis_trade_report_download()
    print("===================================================")
    yuanta_trade_report_download()
    print("===================================================")
    miraeasset_trade_report_download()
    print("===================================================")
    hsbc_trade_report_download()
    print("===================================================")

# if __name__ == "__main__":

#     scheduler = BlockingScheduler()

#     scheduler.add_job(trade_report_download, "cron", day_of_week="mon-fri", hour="17", minute=30)

#     print("Trade report download scheduler executed")
#     scheduler.start()