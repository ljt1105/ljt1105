# 라이브러리 import
import numpy as np
import pandas as pd
from tabulate import tabulate


# 파일 읽어들이기
oms_df = pd.read_excel("C:/PythonProjects/data/20230329_oms.xls", )
trader_df = pd.read_excel("C:/PythonProjects/data/3월29일 거래.xlsx", )

oms_df1 = oms_df[["종목명", "매매유형", "매매구분", "체결수량", "체결단가", "체결금액"]]

oms_df1["매매구분"] = oms_df1[["매매유형", "매매구분"]].agg('_'.join, axis=1)

oms_df1["매매구분"] = oms_df1["매매구분"].replace(['일반_매수', '일반_매도', '차입_매수', '차입_매도'], ['Buy', 'Sell', 'Buy cover', 'Short sell'])

oms_df1 = oms_df1.drop(oms_df1.columns[[1]], axis=1)

oms_df1 = oms_df1.replace(0, np.nan)
oms_df1 = oms_df1.dropna()

col_to_move = oms_df1.pop('매매구분')

oms_df1.insert(1, '매매구분', col_to_move)

oms_df2 = oms_df1.set_index('종목명')

oms_df3 = oms_df2.sort_index(axis=0)

trader_df1 = trader_df[["종목명", "매매구분", "체결수량", "체결단가", "체결금액"]]

trader_df1 = trader_df1.dropna()

trader_df2 = trader_df1.set_index('종목명')

col_to_move2 = trader_df2.pop('매매구분')
price_to_move = trader_df2.pop('체결단가')

col_to_move2 = col_to_move2.reset_index()
price_to_move = price_to_move.reset_index()

col_to_move3 = col_to_move2.drop_duplicates(subset=['종목명'], keep='first')
price_to_move2 = price_to_move.drop_duplicates(subset=['종목명'], keep='first')

col_to_move3 = col_to_move3.set_index('종목명')
price_to_move2 = price_to_move2.set_index('종목명')

trader_df2 = trader_df1.groupby(trader_df1['종목명'], sort=False).sum()

trader_df2 = trader_df2.drop('체결단가', axis=1)
 
trader_df3 = trader_df2.merge(col_to_move3, how='outer', left_index=True, right_index=True)
trader_df3 = trader_df3.merge(price_to_move2, how='outer', left_index=True, right_index=True)

trader_df3 = trader_df3[['매매구분', '체결수량', '체결단가', '체결금액']]

col_to_move3 = col_to_move2.drop_duplicates(subset=['종목명'], keep='first')

trader_df3 = trader_df3.sort_index(axis=0)

trader_df3 = trader_df3.astype({'체결수량' : 'int', '체결단가' : 'int', '체결금액' : 'int'})

trader_df3['체결금액'] = trader_df3['체결금액'].abs()

try:
    trader_df3 = trader_df3.drop(['코스닥150F'])
except:
    pass
try:
    trader_df3 = trader_df3.drop(['코스피200F'])
except:
    pass
try:
    trader_df3 = trader_df3.drop(['코스닥F150'])
except:
    pass
try:
    trader_df3 = trader_df3.drop(['코스피F200'])
except:
    pass

trader_df3 = trader_df3.reset_index()
oms_df3 = oms_df3.reset_index()

result_df = oms_df3

result_df[['종목명']] = oms_df3[['종목명']]
result_df[['매매구분']] = oms_df3[['매매구분']]
result_df[['체결수량']] = oms_df3[['체결수량']] - trader_df3[['체결수량']]
result_df[['체결단가']] = oms_df3[['체결단가']] - trader_df3[['체결단가']]
result_df[['체결금액']] = oms_df3[['체결금액']] - trader_df3[['체결금액']]

result_df[['종목명', '매매구분', '체결단가', '체결수량', '체결금액']]
print(tabulate(oms_df3, headers = 'keys', tablefmt = 'pretty'))
print(tabulate(trader_df3, headers = 'keys', tablefmt = 'pretty'))
print(tabulate(result_df, headers = 'keys', tablefmt = 'pretty'))