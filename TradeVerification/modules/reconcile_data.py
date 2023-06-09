import numpy as np
import pandas as pd
from tabulate import tabulate
import datetime
import time

def reconcile_data(trader_df3, oms_df4, td):
    # trader_df3 = trader_df3.reset_index()
    # oms_df4 = oms_df4.reset_index()



    def get_difference(trader_df3, oms_df4):
        # 두 데이터프레임을 합치고 인덱스를 재설정
        merged_df = trader_df3.merge(oms_df4, how='outer', on=['펀드', '종목명', '매매구분'], suffixes=('_td', '_oms'))

        # 차이를 계산하여 새로운 칼럼에 추가
        merged_df['체결수량_차이'] = merged_df['체결수량_td'] - merged_df['체결수량_oms']
        merged_df['체결단가_차이'] = merged_df['체결단가_td'] - merged_df['체결단가_oms']
        merged_df['체결금액_차이'] = merged_df['체결금액_td'] - merged_df['체결금액_oms']

        return merged_df

    # 두 개의 데이터프레임을 비교하여 차이를 구함
    difference_df = get_difference(trader_df3, oms_df4)

    print("Calculating comlpeted. Showing result")
    time.sleep(1.5)

    print(tabulate(difference_df, headers = 'keys', tablefmt = 'pretty'))
    difference_df.to_excel('Z:/02.펀드/019. 일간매매내역/recon_result/' + td + "_recon_result.xlsx", index=True)
    return difference_df

