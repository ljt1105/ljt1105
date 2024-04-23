import pandas as pd
import numpy as np
import datetime
import os
from pykrx import stock
from openpyxl import load_workbook

def refine_stock_data(opening_df, transaction_df, filtered_ipo_df):

    selected_columns = ['fund_code', 'ticker', 'direction', 'manager', 'stock_name', 'quantity', 'closing_price', 'beginning_gross_amount', 'commission', 'tax']
    start_df = opening_df[selected_columns]

    # 변경할 컬럼 이름 딕셔너리 형태로 저장
    new_column_names = {
        'fund_code' :'fund_code', 
        'ticker' : 'ticker', 
        'direction' : 'pos_direction', 
        'manager' : 'manager', 
        'stock_name' : 'stock_name', 
        'quantity' : 'remained_quantity', 
        'closing_price' : 'entry_price', 
        'beginning_gross_amount' : 'entry_gross_amount',
        'commission' : 'commission',
        'tax' : 'tax'
    }
    start_df.rename(columns=new_column_names, inplace=True)

    # 단축코드 열(column) 선택 후 문자열로 변환 및 6자리 변경하여 저장
    transaction_df.iloc[:, 6] = transaction_df.iloc[:, 6].apply(lambda x: str(x).zfill(6))
    start_df.iloc[:, 1] = start_df.iloc[:, 1].apply(lambda x: str(x).zfill(6))

    # Modify transaction_df based on direction, tax, and commission
    transaction_df["quantity"] = transaction_df.apply(lambda row: f"+{row['quantity']}" if row['tr_direction'] == "Buy" else f"-{row['quantity']}", axis=1)
    transaction_df["gross_amount"] = transaction_df.apply(lambda row: f"-{row['gross_amount']}" if row['tr_direction'] == "Buy" else f"+{row['gross_amount']}", axis=1)
    transaction_df["commission"] = transaction_df.apply(lambda row: f"-{row['commission']}", axis=1)
    transaction_df["tax"] = transaction_df.apply(lambda row: f"-{row['tax']}", axis=1)

    start_df["remained_quantity"] = start_df.apply(lambda row: f"+{row['remained_quantity']}" if row['pos_direction'] == "LONG" else f"-{row['remained_quantity']}", axis=1)
    start_df["entry_gross_amount"] = start_df.apply(lambda row: f"-{row['entry_gross_amount']}" if row['pos_direction'] == "LONG" else f"+{row['entry_gross_amount']}", axis=1)
    start_df["entry_price"] = start_df.apply(lambda row: f"-{row['entry_price']}" if row['pos_direction'] == "LONG" else f"+{row['entry_price']}", axis=1)

    # 숫자로 변환할 열
    columns_to_convert_tr = ['gross_amount', 'quantity', 'commission', 'tax']
    columns_to_convert_st = ['remained_quantity', 'entry_price', 'entry_gross_amount']

    # 숫자로 변환하는 함수 정의
    def convert_to_numeric(column):
        return pd.to_numeric(column, errors='coerce')

    # 함수를 이용하여 숫자로 변환 수행
    transaction_df[columns_to_convert_tr] = transaction_df[columns_to_convert_tr].apply(convert_to_numeric)
    start_df[columns_to_convert_st] = start_df[columns_to_convert_st].apply(convert_to_numeric)

    # transaction_df의 거래를 펀드코드
    sum_df = transaction_df.groupby(['date', 'fund_code', 'fund_name', 'ticker', 'stock_name', 'manager', 'tr_direction'])['quantity', 'gross_amount', 'commission', 'tax'].sum().reset_index()

    # 컬럼 추가 및 값 할당
    sum_df['avg_price'] = sum_df['gross_amount'] / sum_df['quantity']

    sum_df = pd.merge(filtered_ipo_df, sum_df, on={'date', 'fund_code', 'manager', 'direction', 'ticker', 'stock_name', 'quantity', 'avg_price', 'gross_amount', 'commission'})

    # sum_df를 date 순으로 정렬
    sum_df.sort_values(by='date', inplace=True)

    print(sum_df)