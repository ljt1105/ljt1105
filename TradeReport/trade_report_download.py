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
        attachments = message.Attachments

        target_folder = output_dir
        target_folder.mkdir(parents=True, exist_ok=True)

        for attachment in attachments:
            attachment.SaveAsFile(target_folder / str(attachment))

    print("KB-PBS Trade report download complete")


def nh_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/NH")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("NH")
    messages = inbox.Items

    for message in messages:
        attachments = message.Attachments

        target_folder = output_dir
        target_folder.mkdir(parents=True, exist_ok=True)

        for attachment in attachments:
            attachment.SaveAsFile(target_folder / str(attachment))

    print("NH Trade report download complete")


def kis_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/KIS")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("KIS-PBS")
    messages = inbox.Items

    for message in messages:
        attachments = message.Attachments

        target_folder = output_dir
        target_folder.mkdir(parents=True, exist_ok=True)

        for attachment in attachments:
            attachment.SaveAsFile(target_folder / str(attachment))

    print("KIS Trade report download complete")


def yuanta_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/Yuanta")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("Yuanta")
    messages = inbox.Items

    for message in messages:
        attachments = message.Attachments

        target_folder = output_dir
        target_folder.mkdir(parents=True, exist_ok=True)

        for attachment in attachments:
            attachment.SaveAsFile(target_folder / str(attachment))

    print("Yuanta Trade report download complete")


def miraeasset_trade_report_download():
    output_dir = Path("Z:/02.펀드/003.매매보고서 대사/MiraeAsset")
    output_dir.mkdir(parents=True, exist_ok=True)
    outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6).Folders("MiraeAsset")
    messages = inbox.Items

    for message in messages:
        attachments = message.Attachments

        target_folder = output_dir
        target_folder.mkdir(parents=True, exist_ok=True)

        for attachment in attachments:
            attachment.SaveAsFile(target_folder / str(attachment))

    print("MiraeAsset Trade report download complete")


if __name__=="__main__":
    kb_pbs_trade_report_download()
    nh_trade_report_download()
    kis_trade_report_download()
    yuanta_trade_report_download()
    miraeasset_trade_report_download()