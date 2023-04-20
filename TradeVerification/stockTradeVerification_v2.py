# 라이브러리 import
import numpy as np
import pandas as pd
from tabulate import tabulate


# 파일 읽어들이기
oms_df = pd.read_excel("C:/PythonProjects/data/20230419_oms.xls", )
trader_df = pd.read_excel("C:/PythonProjects/data/4월19일 거래.xlsx", )

oms_df1 = oms_df[["펀드", "종목명", "매매유형", "매매구분", "체결수량", "체결단가", "체결금액"]]

oms_df1["매매구분"] = oms_df1[["매매유형", "매매구분"]].agg('_'.join, axis=1)

oms_df1["매매구분"] = oms_df1["매매구분"].replace(['일반_매수', '일반_매도', '차입_매수', '차입_매도'], ['Buy', 'Sell', 'Buy cover', 'Short sell'])

oms_df1 = oms_df1.drop(oms_df1.columns[[2]], axis=1)

oms_df1 = oms_df1.replace(1, np.nan)
oms_df1 = oms_df1.dropna()

col_to_move = oms_df1.pop('매매구분')

oms_df1.insert(2, '매매구분', col_to_move)

oms_df2 = oms_df1.set_index(['펀드', '종목명', '매매구분'])

oms_df3 = oms_df2.sort_index(axis=0)

oms_df3 = oms_df3[(oms_df3 != 0).all(axis=1)]

oms_df4 = oms_df3.groupby(['펀드', '종목명', '매매구분']).agg({'체결수량': 'sum', '체결단가': 'mean', '체결금액': 'sum'})

try:
    trader_df = trader_df[trader_df['매매처'] != 'KIS Swap']
except:
    pass
try:
    trader_df = trader_df[trader_df['매매처'] != 'KB Swap']
except:
    pass

trader_df1 = trader_df[["펀드", "종목명", "매매구분", "체결수량", "체결단가", "체결금액"]]

trader_df1 = trader_df1.dropna()



trader_df2 = trader_df1.set_index('펀드', '종목명', '매매구분')

trader_df3 = trader_df2.groupby(['펀드', '종목명', '매매구분']).agg({'체결수량': 'sum', '체결단가': 'mean', '체결금액': 'sum'})

trader_df3 = trader_df3.sort_index(axis=0)

trader_df3 = trader_df3.astype({'체결수량' : 'int', '체결단가' : 'int', '체결금액' : 'int'})
oms_df4 = oms_df4.astype({'체결수량' : 'int', '체결단가' : 'int', '체결금액' : 'int'})

trader_df3['체결금액'] = trader_df3['체결금액'].abs()

trader_df3 = trader_df3.reset_index()
oms_df4 = oms_df4.reset_index()

try:
    trader_df3 = trader_df3[trader_df3['종목명'] != 'KOSPI200F']
except:
    pass
try:
    trader_df3 = trader_df3[trader_df3['종목명'] != 'KOSDAQ150F']
except:
    pass
try:
    trader_df3 = trader_df3[trader_df3['종목명'] != '코스피200F']
except:
    pass
try:
    trader_df3 = trader_df3[trader_df3['종목명'] != '코스닥150F']
except:
    pass
try:
    trader_df3 = trader_df3[trader_df3['종목명'] != '코스피F200']
except:
    pass
try:
    trader_df3 = trader_df3[trader_df3['종목명'] != '코스닥F150']
except:
    pass



trader_df3 = trader_df3.reset_index()
oms_df4 = oms_df4.reset_index()

result_df = oms_df4
result_df[['종목명']] = oms_df4[['종목명']]
result_df[['매매구분']] = oms_df4[['매매구분']]
result_df[['체결수량']] = oms_df4[['체결수량']] - trader_df3[['체결수량']]
result_df[['체결단가']] = oms_df4[['체결단가']] - trader_df3[['체결단가']]
result_df[['체결금액']] = oms_df4[['체결금액']] - trader_df3[['체결금액']]

print(tabulate(result_df, headers = 'keys', tablefmt = 'pretty'))