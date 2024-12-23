import pandas as pd
from tabulate import tabulate
from pykrx import stock
from datetime import datetime, timedelta

def read_prelude_stock_trade_history():

    today = datetime.now().strftime("%m%d%y")

    file_path = "Z:/02.펀드/003.매매보고서 대사/PRELUDE_RECAP/Korea Stocks - 122024.xls"
    df = pd.read_excel(file_path)

    # 2. 필요한 칼럼만 남기기
    columns_to_keep = [
        'Client Account Name', 'Buy/Sell', 'Ric', 'Stock Description', 'Price (Gross) Listing Ccy', 'Stock Quantity'
    ]
    df = df[columns_to_keep]

    # 3. 칼럼 이름 변경
    df.columns = ['펀드명', '매매구분', '종목코드', '종목명', '체결가격', '체결수량']

    # 4. 종목코드 앞의 여섯 자리만 남기기
    df['종목코드'] = df['종목코드'].astype(str).str[:6]

    # 5. 매매금액 칼럼 추가 (체결가격 * 체결수량)
    df['매매금액'] = df['체결가격'] * df['체결수량']

    # 6. 펀드명 데이터를 'Prelude'로 변경
    df['펀드명'] = 'Prelude'

    # 7. 매매구분 값을 변환 (Buy -> 매수, Sell -> 매도)
    df['매매구분'] = df['매매구분'].replace({'Buy': '매수', 'Sell': '매도'})

    prelude_stock_df = df

    print(tabulate(df, headers = 'keys', tablefmt = 'pretty'))

    return prelude_stock_df


def main():
    read_prelude_stock_trade_history()

if __name__ == "__main__":
    main()