import pandas as pd
from tabulate import tabulate
from pykrx import stock
from datetime import datetime, timedelta

def read_ms_stock_recap():

    today = datetime.now().strftime("%m%d%y")

    file_path = f"Z:/02.펀드/003.매매보고서 대사/PRELUDE_RECAP/Korea Stocks - {today}.xls"
    df = pd.read_excel(file_path)

    # 2. 필요한 칼럼만 남기기
    columns_to_keep = [
        'Client Account Name', 'Buy/Sell', 'Ric', 'Stock Description', 'Price (Gross) Listing Ccy', 'Stock Quantity'
    ]
    df = df[columns_to_keep]

    # 3. 칼럼 이름 변경
    df.columns = ['펀드명', '매매구분', '단축코드', '종목명', '체결단가', '체결수량']

    # 4. 종목코드 앞의 여섯 자리만 남기기
    df['단축코드'] = df['단축코드'].astype(str).str[:6]

    # 5. 매매금액 칼럼 추가 (체결가격 * 체결수량)
    df['체결금액'] = df['체결단가'] * df['체결수량']

    # 6. 펀드명 데이터를 'Prelude'로 변경
    df['펀드명'] = 'Prelude'

    # 7. 매매구분 값을 변환 (Buy -> 매수, Sell -> 매도)
    df['매매구분'] = df['매매구분'].replace({'Buy': '매수', 'Sell': '매도'})

    ms_recap_stock_df = df

    print(tabulate(ms_recap_stock_df, headers = 'keys', tablefmt = 'pretty'))

    return ms_recap_stock_df


def read_oms_cfd_history():

    today = datetime.now().strftime("%Y-%m-%d")

    file_path = f"Z:/02.펀드/019. 일간매매내역/prelude/{today}_stock.xlsx"
    df = pd.read_excel(file_path)

    # 2. 필요한 칼럼만 남기기
    columns_to_keep = [
        '펀드명', '포지션', 'BBIC', '종목명', '체결단가', '체결수량', '체결금액'
    ]
    df = df[columns_to_keep]

    # 3. 칼럼 이름 변경
    df.columns = ['펀드명', '매매구분', '단축코드', '종목명', '체결단가', '체결수량', '체결금액']

    # 4. 종목코드 앞의 여섯 자리만 남기기
    df['단축코드'] = df['단축코드'].astype(str).str.zfill(6)

    # 6. 펀드명 데이터를 'Prelude'로 변경
    df['펀드명'] = 'Prelude'

    # 7. 매매구분 값을 변환 (Buy -> 매수, Sell -> 매도)
    df['매매구분'] = '매수'

    oms_stock_df = df

    print(tabulate(oms_stock_df, headers = 'keys', tablefmt = 'pretty'))

    return oms_stock_df


def merge_and_reconcile(output_path):
    # OMS Futures와 Stock 데이터를 읽기
    oms_cfd_df = read_oms_cfd_history()
    ms_stock_df = read_ms_stock_recap()

    # 2. 대사 작업: 펀드명, 매매구분, 단축코드가 일치하는 행에서 체결단가, 체결수량, 체결금액 비교
    reconciliation_df = oms_cfd_df.merge(
        ms_stock_df,
        on=['펀드명', '매매구분', '단축코드'],
        suffixes=('_oms', '_ms'),
        how='outer',
        indicator=True
    )

    # 체결단가, 체결수량, 체결금액의 차이 계산
    reconciliation_df['체결단가_차이'] = reconciliation_df['체결단가_oms'] - reconciliation_df['체결단가_ms']
    reconciliation_df['체결수량_차이'] = reconciliation_df['체결수량_oms'] - reconciliation_df['체결수량_ms']
    reconciliation_df['체결금액_차이'] = reconciliation_df['체결금액_oms'] - reconciliation_df['체결금액_ms']

    # 종목명 유지: Trader의 종목명을 우선 사용, 없으면 OMS의 종목명을 사용
    reconciliation_df['종목명'] = reconciliation_df['종목명_ms'].combine_first(reconciliation_df['종목명_oms'])

    # 필요 없는 종목명 관련 컬럼 제거
    reconciliation_df.drop(columns=['종목명_ms', '종목명_oms'], inplace=True, errors='ignore')

    # 결과 출력
    print("대사 결과:")
    # print(reconciliation_df[['펀드명', '매매구분', '종목명', '체결단가_차이', '체결수량_차이', '체결금액_차이']])
    print(tabulate(reconciliation_df[['펀드명', '매매구분', '단축코드', '종목명', '체결단가_차이', '체결수량_차이', '체결금액_차이']], headers = 'keys', tablefmt = 'pretty'))

    # 결과를 파일로 저장 (옵션)
    reconciliation_df.to_excel(output_path, index=False)

    return reconciliation_df

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    # read_ms_stock_recap()
    # read_oms_cfd_history()
    output_path = f'Z:/02.펀드/019. 일간매매내역/recon_result/{today}_prelude recon result.xlsx'
    merge_and_reconcile(output_path)

if __name__ == "__main__":
    main()