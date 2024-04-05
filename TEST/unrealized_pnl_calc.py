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
transaction_sheet = 'transaction' 
start_sheet = 'start'

# Read each sheet from position.xlsx and save to dataframe
transaction_df = pd.read_excel(file_path, sheet_name=transaction_sheet)
opening_df = pd.read_excel(file_path, sheet_name=start_sheet)

selected_columns = ['fund_code', 'ticker', 'direction', 'manager', 'stock_name', 'quantity', 'closing_price', 'beginning_gross_amount', 'commission', 'tax']
start_df = opening_df[selected_columns]

# 통합된 데이터프레임을 엑셀 파일로 저장
output_file = os.path.join(file_path, 'output_df.xlsx')
start_df.to_excel(file_path, index=False)

# # 변경할 컬럼 이름 딕셔너리 형태로 저장
# new_column_names = {
#     'fund_code' :'fund_code', 
#     'ticker' : 'ticker', 
#     'direction' : 'direction', 
#     'manager' : 'manager', 
#     'stock_name' : 'stock_name', 
#     'quantity' : 'quantity', 
#     'closing_price' : 'entry_price', 
#     'beginning_gross_amount' : 'entry_gross_amount',
#     'commission' : 'commission',
#     'tax' : 'tax'
# }
# start_df.rename(columns=new_column_names, inplace=True)

# # 단축코드 열(column) 선택 후 문자열로 변환 및 6자리 변경하여 저장
# transaction_df.iloc[:, 6] = transaction_df.iloc[:, 6].apply(lambda x: str(x).zfill(6))
# start_df.iloc[:, 1] = start_df.iloc[:, 1].apply(lambda x: str(x).zfill(6))

# # Modify transaction_df based on direction, tax, and commission
# transaction_df["quantity"] = transaction_df.apply(lambda row: f"+{row['quantity']}" if row['direction'] == "Buy" else f"-{row['quantity']}", axis=1)
# transaction_df["gross_amount"] = transaction_df.apply(lambda row: f"-{row['gross_amount']}" if row['direction'] == "Buy" else f"+{row['gross_amount']}", axis=1)
# transaction_df["commission"] = transaction_df.apply(lambda row: f"-{row['commission']}", axis=1)
# transaction_df["tax"] = transaction_df.apply(lambda row: f"-{row['tax']}", axis=1)

# start_df["quantity"] = start_df.apply(lambda row: f"+{row['quantity']}" if row['direction'] == "Buy" else f"-{row['quantity']}", axis=1)
# start_df["entry_gross_amount"] = start_df.apply(lambda row: f"-{row['entry_gross_amount']}" if row['direction'] == "Buy" else f"+{row['entry_gross_amount']}", axis=1)
# start_df["entry_price"] = start_df.apply(lambda row: f"-{row['entry_price']}" if row['direction'] == "Buy" else f"+{row['entry_price']}", axis=1)

# # 숫자로 변환할 열
# columns_to_convert_tr = ['gross_amount', 'quantity', 'commission', 'tax']
# columns_to_convert_st = ['quantity', 'entry_price', 'entry_gross_amount']

# # 숫자로 변환하는 함수 정의
# def convert_to_numeric(column):
#     return pd.to_numeric(column, errors='coerce')

# # 함수를 이용하여 숫자로 변환 수행
# transaction_df[columns_to_convert_tr] = transaction_df[columns_to_convert_tr].apply(convert_to_numeric)
# start_df[columns_to_convert_st] = start_df[columns_to_convert_st].apply(convert_to_numeric)

# # 미실현 손익을 저장할 데이터프레임 정의
# unrealized_pnl_df = pd.DataFrame(columns=['fund_code', 'fund_name', 'ticker', 'stock_name', 'direction', 'manager', 
#                                           'quantity', 'entry_price', 'entry_gross_amount', 'current_price', 'current_value', 
#                                           'commission', 'tax', 'net_pnl'])

# # 인덱스 설정
# unrealized_pnl_df.set_index(['fund_code', 'fund_name', 'ticker', 'stock_name', 'direction', 'manager', 
#                              'quantity', 'entry_price', 'entry_gross_amount', 'current_price', 'current_value', 
#                              'commission', 'tax', 'net_pnl'], inplace=True)

# sum_df = transaction_df.groupby(['fund_code', 'ticker', 'manager'])['quantity', 'gross_amount', 'commission', 'tax'].sum().reset_index()

# # sum_df를 기준으로 start_df 업데이트 및 unrealized_pnl_df 추가
# for index, row in sum_df.iterrows():
#     mask = (start_df['fund_code'] == row['fund_code']) & (start_df['ticker'] == row['ticker']) & (start_df['manager'] == row['manager'])
#     matching_rows = start_df[mask]
    
#     # 일치하는 행이 존재하면 해당 데이터 업데이트
#     if not matching_rows.empty:
#         start_df.loc[matching_rows.index, 'quantity'] += row['quantity']
#         start_df.loc[matching_rows.index, 'entry_gross_amount'] += row['gross_amount']
#         start_df.loc[matching_rows.index, 'commission'] += row['commission']
#         start_df.loc[matching_rows.index, 'tax'] += row['tax']  

#         # Reset index of matching_rows
#         matching_rows.reset_index(drop=True, inplace=True)

#         # 복사할 열을 unrealized_pnl_df에 추가
#         start_df_columns = ['direction', 'stock_name', 'entry_price', 'entry_gross_amount', 'commission', 'tax']
#         for col in start_df_columns:
#             unrealized_pnl_df[col] = None
#             unrealized_pnl_df.loc[matching_rows.index, col] = matching_rows[col].values

#     # 일치하는 행이 없으면 unrealized_pnl_df에 새로운 행 추가
#     else:
#         unrealized_pnl_df = unrealized_pnl_df.append(row, ignore_index=True)

# # current_prices 리스트 초기화
# current_prices = []

# # stock_info와 unrealized_pnl_df를 통해 종가 데이터 일치 여부 확인
# for ticker in unrealized_pnl_df['ticker']:
#     try:
#         # stock_info에서 ticker와 동일한 행 선택
#         matching_row = stock_info.loc[stock_info.index == ticker]

#         # 해당 행에서 종가 데이터 가져오기
#         close_price = matching_row['종가'].values[0]

#         # current_prices 리스트에 종가 데이터 추가
#         current_prices.append(close_price)
#     except Exception as e:
#         print(f"Error fetching data for ticker {ticker}: {e}")
#         current_prices.append(None)  # 에러가 발생하면 None으로 처리

# # unrealized_pnl_df의 current_price 컬럼에 current_prices 데이터 할당
# unrealized_pnl_df['current_price'] = current_prices

# #계산
# unrealized_pnl_df['entry_price'] = unrealized_pnl_df['entry_gross_amount'] / unrealized_pnl_df['quantity']
# unrealized_pnl_df['current_value'] = unrealized_pnl_df['quantity'] * unrealized_pnl_df['current_price']
# unrealized_pnl_df['net_pnl'] = unrealized_pnl_df['gross_amount'] + unrealized_pnl_df['current_value']

# # 결과를 'unrealized_pnl' 시트에 저장
# with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
#     unrealized_pnl_df.to_excel(writer, sheet_name='unrealized_pnl', index=False)