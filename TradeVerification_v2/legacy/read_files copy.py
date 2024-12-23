import pandas as pd
from tabulate import tabulate
from pykrx import stock
from datetime import datetime, timedelta



def read_oms_futures_file():
    # 1. 엑셀 파일 불러오기
    file_path = 'Z:/02.펀드/019. 일간매매내역/test/파생/2024-12-19_futures.xlsx'  # 파일 경로를 적절히 수정하세요.
    df = pd.read_excel(file_path)

    # 2. 필요한 칼럼만 남기기
    columns_to_keep = ['펀드명', '매매\n구분', '종목코드', '종목명', '체결단가', '체결\n계약수', '약정금액']
    df = df[columns_to_keep]

    # 칼럼 이름 정리
    df.columns = ['펀드명', '매매구분', '종목코드', '종목명', '체결단가', '체결계약수', '약정금액']

    # 3. 펀드명 변환
    fund_name_mapping = {
        "두나미스 공모주 일반사모투자신탁": "공모주1호",
        "두나미스 공모주 일반사모투자신탁 제2호": "공모주2호",
        "두나미스 공모주 포커스 일반사모투자신탁": "포커스",
        "두나미스 공모주 알파 일반사모투자신탁 운": "알파",
        "두나미스 코스닥벤처 일반사모투자신탁": "코스닥벤처1호",
        "두나미스 코스닥벤처 일반사모투자신탁 2호": "코스닥벤처2호",
        "두나미스 코스닥벤처 일반사모투자신탁 3호": "코스닥벤처3호",
        "두나미스 멀티전략 일반사모(운)": "멀티전략",
        "두나미스 블록딜 공모주 일반사모투자신탁": "블록딜",
        "DUNAMIS_PRELUDE 일임 (USD)": "Prelude"
    }
    df['펀드명'] = df['펀드명'].replace(fund_name_mapping)

    # 4. 종목코드 변환 (앞 3자리와 뒤 5자리만 남기기)
    df['종목코드'] = df['종목코드'].str[3:8]

    # 단축코드 6자리로 수정
    df['종목코드'] = df['종목코드'].astype(str).str.zfill(6)

    # 5. 칼럼 이름 변경
    column_rename_mapping = {
        "종목코드": "단축코드",
        "체결계약수": "체결수량",
        "약정금액": "체결금액"
    }
    df.rename(columns=column_rename_mapping, inplace=True)

    # 6. 가공된 데이터프레임 저장
    oms_futures_df = df

    # 결과 확인
    print(tabulate(oms_futures_df, headers = 'keys', tablefmt = 'pretty'))

    return oms_futures_df


def read_oms_stock_file():
    # 1. 엑셀 파일 불러오기
    file_path = 'Z:/02.펀드/019. 일간매매내역/test/주식/2024-12-19_stock.xlsx'  # 파일 경로를 적절히 수정하세요.
    df = pd.read_excel(file_path)

    # 2. 필요한 칼럼만 남기기
    columns_to_keep = ['펀드명', '매매구분', '종목명', '체결가격', '체결수량', '매매금액']
    df = df[columns_to_keep]

    # 3. 펀드명 변환
    fund_name_mapping = {
        "두나미스 공모주 일반사모투자신탁": "공모주1호",
        "두나미스 공모주 일반사모투자신탁 제2호": "공모주2호",
        "두나미스 공모주 포커스 일반사모투자신탁": "포커스",
        "두나미스 공모주 알파 일반사모투자신탁 운용": "알파",
        "두나미스 코스닥벤처 일반사모투자신탁": "코스닥벤처1호",
        "두나미스 코스닥벤처 일반사모투자신탁 2호": "코스닥벤처2호",
        "두나미스 코스닥벤처 일반사모투자신탁 3호": "코스닥벤처3호",
        "두나미스 멀티전략 일반사모(운)": "멀티전략",
        "두나미스 블록딜공모주 일반사모투자신탁 1호(운용)": "블록딜",
        "DUNAMIS_PRELUDE 일임 (USD)": "Prelude"
    }
    df['펀드명'] = df['펀드명'].replace(fund_name_mapping)

    # 종목명 클렌징
    df['종목명'] = df['종목명'].str.strip()

    # 4. pykrx를 사용해 종목명으로 단축코드 생성
    today = datetime.now()
    date = (today - timedelta(days=1)).strftime("%Y%m%d")  # 어제 날짜
    
    # 코스피 및 코스닥 종목코드 가져오기
    kospi_stocks = stock.get_market_ticker_list(date=date, market="KOSPI")
    kosdaq_stocks = stock.get_market_ticker_list(date=date, market="KOSDAQ")

    kospi_mapping = {stock.get_market_ticker_name(ticker): ticker for ticker in kospi_stocks}
    kosdaq_mapping = {stock.get_market_ticker_name(ticker): ticker for ticker in kosdaq_stocks}
    # 두 시장의 매핑 통합
    stock_code_mapping = {**kospi_mapping, **kosdaq_mapping}

    # 종목명으로 단축코드 매핑
    df['단축코드'] = df['종목명'].map(stock_code_mapping)
    
    # 매핑되지 않은 종목명 확인
    unmatched = df[df['단축코드'].isna()]['종목명'].unique()
    if unmatched.size > 0:
        print("매핑되지 않은 종목명:", unmatched)

    # 단축코드 칼럼을 종목명 앞에 배치
    df = df[['펀드명', '매매구분', '단축코드', '종목명', '체결가격', '체결수량', '매매금액']]

    # 5. 칼럼 이름 변경
    df.rename(columns={
        "체결가격": "체결단가",
        "매매금액": "체결금액"
    }, inplace=True)

    # 6. 가공된 데이터프레임 저장
    oms_stock_df = df

    # 결과 확인
    print(tabulate(oms_stock_df, headers = 'keys', tablefmt = 'pretty'))

    return oms_stock_df


def read_trader_file():

    # 1. 엑셀 파일 불러오기
    file_path = 'Z:/02.펀드/019. 일간매매내역/12월19일 전체.xlsx'  # 파일 경로를 적절히 수정하세요.
    df = pd.read_excel(file_path)

    # 2. 필요한 칼럼만 남기기
    columns_to_keep = ['펀드', '매매구분', '단축코드', '종목명', '체결단가', '체결수량', '체결금액']
    df = df[columns_to_keep]

    # 3. 단축코드 6자리로 수정
    df['단축코드'] = df['단축코드'].astype(str).str.zfill(6)

    # 4. 칼럼 이름 변경
    df.rename(columns={
        "펀드": "펀드명"
    }, inplace=True)

    # 5. 매매구분 변환
    direction_mapping = {
        "Buy": "매수",
        "Sell": "매도"
    }
    df['매매구분'] = df['매매구분'].replace(direction_mapping)

    # 데이터프레임 저장
    trader_df = df

    print(tabulate(trader_df, headers = 'keys', tablefmt = 'pretty'))

    return trader_df


def merge_and_reconcile():
    # OMS Futures와 Stock 데이터를 읽기
    oms_futures_df = read_oms_futures_file()
    oms_stock_df = read_oms_stock_file()

    # 1. oms_futures_df를 oms_stock_df 아래에 병합
    combined_df = pd.concat([oms_stock_df, oms_futures_df], ignore_index=True)

    # Trader 데이터를 읽기
    trader_df = read_trader_file()

    # 2. 대사 작업: 펀드명, 매매구분, 단축코드가 일치하는 행에서 매칭
    matched_rows = []

    # 각 OMS 행을 순회하며 1:1 매칭 수행
    for _, oms_row in combined_df.iterrows():
        # 펀드명, 매매구분, 단축코드가 일치하는 Trader 행 필터링
        candidates = trader_df[
            (trader_df['펀드명'] == oms_row['펀드명']) &
            (trader_df['매매구분'] == oms_row['매매구분']) &

            (trader_df['단축코드'] == oms_row['단축코드'])
        ]

        if not candidates.empty:
            # 체결단가, 체결수량, 체결금액의 최소 차이로 가장 근접한 행 선택
            candidates['차이_합계'] = (
                abs(candidates['체결단가'] - oms_row['체결단가']) +
                abs(candidates['체결수량'] - oms_row['체결수량']) +
                abs(candidates['체결금액'] - oms_row['체결금액'])
            )
            best_match = candidates.loc[candidates['차이_합계'].idxmin()]
            matched_rows.append({
                '펀드명': oms_row['펀드명'],
                '매매구분': oms_row['매매구분'],
                '단축코드': oms_row['단축코드'],
                'OMS_체결단가': oms_row['체결단가'],
                'OMS_체결수량': oms_row['체결수량'],
                'OMS_체결금액': oms_row['체결금액'],
                'TRADER_체결단가': best_match['체결단가'],
                'TRADER_체결수량': best_match['체결수량'],
                'TRADER_체결금액': best_match['체결금액'],
            })

    # 매칭 결과를 DataFrame으로 변환
    reconciliation_df = pd.DataFrame(matched_rows)

    # 차이 계산
    reconciliation_df['체결단가_차이'] = reconciliation_df['OMS_체결단가'] - reconciliation_df['TRADER_체결단가']
    reconciliation_df['체결수량_차이'] = reconciliation_df['OMS_체결수량'] - reconciliation_df['TRADER_체결수량']
    reconciliation_df['체결금액_차이'] = reconciliation_df['OMS_체결금액'] - reconciliation_df['TRADER_체결금액']

    # 결과 출력
    print("1:1 대사 결과:")
    print(reconciliation_df)

    # 결과를 파일로 저장
    reconciliation_df.to_excel("reconciliation_result_1to1.xlsx", index=False)

    return reconciliation_df

def main():
    # read_oms_futures_file()
    # read_oms_stock_file()
    # read_trader_file()
    merge_and_reconcile()

if __name__ == "__main__":
    main()