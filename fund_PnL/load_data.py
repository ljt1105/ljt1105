import pandas as pd
import numpy as np
import datetime
import os
from pykrx import stock
from openpyxl import load_workbook

def load_beginning_transacion_data():
    # 코드 돌리는 당일 날짜 저장
    today = datetime.datetime.today().strftime('%Y%m%d')

    # 주식 데이터 저장
    stock_info = stock.get_market_ohlcv_by_ticker(today)

    # 엑셀파일 경로 저장 및 읽어들일 시트 이름 설정
    file_path = r'C:\PythonProjects\recon\positions.xlsx'

    # Read each sheet from positions.xlsx and save to dataframe
    transaction_df = pd.read_excel(file_path, sheet_name='transaction')
    opening_df = pd.read_excel(file_path, sheet_name='start')

    return transaction_df, opening_df