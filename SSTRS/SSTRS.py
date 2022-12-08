import download
import classify
import copy
import mr_download

if __name__ == "__main__":
    print("==============================================")
    download.download_files()
    print("==============================================")
    mr_download.margin_report_download()
    print("==============================================")
    classify.classify_files()
    print("==============================================")
    copy.copy_files()
    print("==============================================")