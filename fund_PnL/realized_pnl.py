import pandas as pd
import numpy as np
import datetime
import os
from pykrx import stock
from openpyxl import load_workbook


# 펀드, 매니저, 종목(종목명, 종목코드) 기준으로 realized_pnl합산
# def calculating_realized_pnl():
file_path = r'C:\PythonProjects\recon\daily_output.xlsx'
df = pd.read_excel(file_path, header=0, engine="openpyxl")

# pnl 칼럼의 데이터 타입을 실수형으로 변환
df['pnl'] = pd.to_numeric(df['pnl'], errors='coerce')

sum_realized_pnl_df = df.groupby(['fund_code', 'manager', 'ticker', 'stock_name']).agg({'pnl': 'sum'}).reset_index()

# 4번째 열(column) 선택 후 문자열로 변환하여 저장
sum_realized_pnl_df.iloc[:, 2] = sum_realized_pnl_df.iloc[:, 2].apply(lambda x: str(x).zfill(6))


print(sum_realized_pnl_df)

sum_realized_pnl_df.to_excel('C:/PythonProjects/recon/cal_pnl.xlsx', index=False)