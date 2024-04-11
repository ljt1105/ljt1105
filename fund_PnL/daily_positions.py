import pandas as pd
import datetime
import os
from pykrx import stock
from openpyxl import load_workbook

# 코드 돌리는 당일 날짜 저장
today = datetime.datetime.today().strftime('%Y%m%d')

# 주식 데이터 저장
stock_info = stock.get_market_ohlcv_by_ticker(today)

# 엑셀파일 경로 저장 및 읽어들일 시트 이름 설정
file_path = r'C:\PythonProjects\recon\positions.xlsx'

# Read each sheet from position.xlsx and save to dataframe
transaction_df = pd.read_excel(file_path, sheet_name='transaction')
opening_df = pd.read_excel(file_path, sheet_name='start')

selected_columns = ['fund_code', 'ticker', 'direction', 'manager', 'stock_name', 'quantity', 'closing_price', 'beginning_gross_amount', 'commission', 'tax']
start_df = opening_df[selected_columns]

# 변경할 컬럼 이름 딕셔너리 형태로 저장
new_column_names = {
    'fund_code' :'fund_code', 
    'ticker' : 'ticker', 
    'direction' : 'direction', 
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
transaction_df["quantity"] = transaction_df.apply(lambda row: f"+{row['quantity']}" if row['direction'] == "Buy" else f"-{row['quantity']}", axis=1)
transaction_df["gross_amount"] = transaction_df.apply(lambda row: f"-{row['gross_amount']}" if row['direction'] == "Buy" else f"+{row['gross_amount']}", axis=1)
transaction_df["commission"] = transaction_df.apply(lambda row: f"-{row['commission']}", axis=1)
transaction_df["tax"] = transaction_df.apply(lambda row: f"-{row['tax']}", axis=1)

start_df["remained_quantity"] = start_df.apply(lambda row: f"+{row['remained_quantity']}" if row['direction'] == "Buy" else f"-{row['remained_quantity']}", axis=1)
start_df["entry_gross_amount"] = start_df.apply(lambda row: f"-{row['entry_gross_amount']}" if row['direction'] == "Buy" else f"+{row['entry_gross_amount']}", axis=1)
start_df["entry_price"] = start_df.apply(lambda row: f"-{row['entry_price']}" if row['direction'] == "Buy" else f"+{row['entry_price']}", axis=1)

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
sum_df = transaction_df.groupby(['date', 'fund_code', 'fund_name', 'ticker', 'stock_name', 'manager', 'direction'])['quantity', 'gross_amount', 'commission', 'tax'].sum().reset_index()

# 컬럼 추가 및 값 할당
sum_df['avg_price'] = sum_df['gross_amount'] / sum_df['quantity']

# sum_df를 date 순으로 정렬
sum_df.sort_values(by='date', inplace=True)

# # start_df를 복제하여 미실현 수익이 계산 및 저장될 새로운 데이터프레임 생성
# pnl_cal_df = start_df.copy()

# # gross_amount 컬럼을 추가하여 복제된 데이터프레임에 할당
# pnl_cal_df['gross_amount'] = pnl_cal_df['remained_quantity'] * pnl_cal_df['entry_price']

# 이전 포지션 초기화
previous_position = start_df.copy()
previous_position['date'] = pd.to_datetime('2024-01-01')  # 초기 날짜 설정
previous_position['net_amount'] = previous_position['entry_gross_amount'] + previous_position['commission'] + previous_position['tax']
previous_position['gross_amount'] = previous_position['entry_gross_amount']

# daily_position_df 초기화
daily_position_df = pd.DataFrame(columns=['date', 'fund_code', 'manager', 'ticker', 'stock_name', 'remained_quantity', 
                                        'remained_amount', 'traded_quantity', 'traded_amount', 'commission', 'tax', 'net_amount'])

# 초기 포지션 정보를 daily_position_df에 추가
daily_position_df = pd.concat([daily_position_df, previous_position], ignore_index=False)

# previous_position에도 초기 포지션 정보 추가
# previous_position = pd.DataFrame(initial_position_info, index=[0])

# 날짜별로 반복하면서 포지션 계산
for index, row in sum_df.iterrows():
    # 현재 거래 내역 가져오기
    date = row['date']
    fund_code = row['fund_code']
    manager = row['manager']
    ticker = row['ticker']
    stock_name = row['stock_name']
    direction = row['direction']
    quantity = row['quantity']
    gross_amount = row['gross_amount']
    commission = row['commission']
    tax = row['tax']
    
    # 이전 포지션에서 해당 종목의 이전 정보 가져오기
    previous_info = previous_position[(previous_position['fund_code'] == fund_code) & (previous_position['ticker'] == ticker) & (previous_position['manager'] == manager)]

    if not previous_info.empty:
        previous_quantity = previous_info.iloc[0]['remained_quantity']
        previous_gross_amount = previous_info.iloc[0]['gross_amount']
        previous_commission = previous_info.iloc[0]['commission']
        previous_tax = previous_info.iloc[0]['tax']
    else:
        previous_quantity = 0
        previous_gross_amount = 0
        previous_commission = 0
        previous_tax = 0
    
    # 남은 포지션 계산
    remained_quantity = previous_quantity + quantity
    remained_amount = previous_gross_amount + gross_amount
    commission = previous_commission + commission
    tax = previous_tax + tax
    net_amount = gross_amount + commission + tax
    
    # 남은 포지션 정보 업데이트
    position_info = {
        'date': date,
        'fund_code': fund_code,
        'manager': manager,
        'ticker': ticker,
        'stock_name': stock_name,
        'direction': direction,
        'remained_quantity': remained_quantity,
        'remained_amount': remained_amount,
        'traded_quantity': quantity,
        'traded_amount': gross_amount,
        'commission': commission,
        'tax': tax,
        'net_traded_amount': net_amount
        
    }
    
    # daily_position_df에 추가
    # daily_position_df = daily_position_df.append(position_info, ignore_index=True)
    daily_position_df = pd.concat([daily_position_df, pd.DataFrame(position_info, index=[0])], ignore_index=True)
    
    # 이전 포지션 업데이트
    # previous_position = previous_position.append(position_info, ignore_index=True)
    previous_position = pd.concat([previous_position, pd.DataFrame(position_info, index=[0])], ignore_index=True)


    # remained_quantity가 0이 되면 해당 행 삭제
    if remained_quantity == 0:
        previous_position = previous_position.drop(previous_position[(previous_position['fund_code'] == fund_code) & (previous_position['ticker'] == ticker) & (previous_position['manager'] == manager)].index)

# 날짜 형식 변환
daily_position_df['date'] = pd.to_datetime(daily_position_df['date']).dt.date


daily_position_df.to_excel('C:/PythonProjects/recon/daily_output.xlsx', index=False)