import pandas as pd
import numpy as np
import datetime
import os
from pykrx import stock
from openpyxl import load_workbook

def load_ipo_stock_data():

    ipo_file_path = r'C:\PythonProjects\recon\청약내역_펀드.xlsx'

    ipo_df = pd.read_excel(ipo_file_path, sheet_name='Sheet1')

    # ipo_df에서 2024년 상장예정인 종목만 남기고 모두 삭제
    ipo_df.columns = ipo_df.iloc[0] # 첫번째 행을 컬럼명으로 지정
    ipo_df = ipo_df.iloc[1:]

    ipo_df['상장예정일'] = pd.to_datetime(ipo_df['상장예정일'])
    filtered_ipo_df = ipo_df[ipo_df['상장예정일'].dt.year == 2024]

    ipo_selected_columns = ['펀드', 'Ticker', '종목명', '배정수량', '단가', '청약금액', '수수료', '상장예정일']

    filtered_ipo_df = filtered_ipo_df[ipo_selected_columns]

    new_column_names = {
        '상장예정일' : 'date',
        'Ticker' : 'ticker',
        '펀드' : 'fund_code',
        '종목명' : 'stock_name',
        '배정수량' : 'quantity',
        '단가' : 'avg_price',
        '청약금액' : 'gross_amount',
        '수수료' : 'commission'
    }

    filtered_ipo_df.rename(columns=new_column_names, inplace=True)

    filtered_ipo_df = filtered_ipo_df[filtered_ipo_df['fund_code'] != 'BVI']
    filtered_ipo_df['manager'] = '김대욱'
    filtered_ipo_df['tr_direction'] = 'Buy'

    columns_to_convert = ['quantity', 'avg_price', 'gross_amount', 'commission']

    def convert_to_numeric(column):
        return pd.to_numeric(column, errors='coerce')

    filtered_ipo_df[columns_to_convert] = filtered_ipo_df[columns_to_convert].apply(convert_to_numeric)

    return filtered_ipo_df