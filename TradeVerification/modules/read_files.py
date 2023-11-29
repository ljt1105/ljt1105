import numpy as np
import pandas as pd
from tabulate import tabulate
import datetime


def read_df_files():
    # 현재 날짜 가져오기
    current_date = datetime.datetime.now()

    # yyyymmdd 형식으로 변환
    td = current_date.strftime("%Y%m%d")
    # td = "20230607"

    td_tr1 = current_date.strftime("%Y").lstrip("0")
    td_tr2 = current_date.strftime("%m").lstrip("0")
    td_tr3 = current_date.strftime("%d").lstrip("0")

    #td_tr1 = current_date.strftime("%Y")
    #td_tr2 = current_date.strftime("%m")
    #td_tr3 = current_date.strftime("%d")

    td_tr = td_tr2 + "월" + td_tr3 + "일"
    # td_tr = "9월14일"

    print("Today : " + td_tr)


    oms_df = pd.read_excel("Z:/02.펀드/019. 일간매매내역/" + td + "_oms.xls", )
    trader_df = pd.read_excel("Z:/02.펀드/019. 일간매매내역/" + td_tr + " 거래.xlsx", )

    print("File load completed")

    return oms_df, trader_df, td, td_tr