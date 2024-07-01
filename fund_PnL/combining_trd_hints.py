# HINTs #22713에서 받은 기간내 거래내역 불러오기 및 result_df.xlsx와 정보 매칭 작업
# 해당 작업은 oms 및 trade팀의 부정확한 단가 및 거래금액, 수수료, 거래세를 교정하기 위한 작업

# 필요한 라이브러리 불러오기
import pandas as pd
import datetime
from openpyxl import load_workbook

def combining_trd_hints_data():

    # 당일 날짜 저장
    # now = datetime.datetime.today().strftime('%Y-%m-%d')

    # 어제 날짜 저장
    now = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print("어제 날짜 : " + now)

    # 거래내역 위치 저장
    file_path_df1 = "C:\\PythonProjects\\recon\\hints\\" + now + ".xlsx"
    file_path_df2 = r'C:\PythonProjects\recon\result_df.xlsx'

    # 당일 거래내역 데이터프레임으로 저장
    df1 = pd.read_excel(file_path_df1, header=0)
    df2 = pd.read_excel(file_path_df2, header=0)

    # '종목명' 열이 'NaN'인 행 삭제
    df1 = df1.dropna(subset=['종목명'])

    # 매매처명 통일
    df1.loc[df1['매매처명'] == '한국투자증권', '매매처명'] = 'KIS'
    df1.loc[df1['매매처명'] == '유안타증권', '매매처명'] = 'Yuanta'
    df1.loc[df1['매매처명'] == 'CGS-CIMB증권(한국지점)', '매매처명'] = 'CGSI'
    df1.loc[df1['매매처명'] == 'CLSA증권', '매매처명'] = 'CLSA'
    df1.loc[df1['매매처명'] == 'HSBC증권', '매매처명'] = 'HSBC'
    df1.loc[df1['매매처명'] == 'KB증권', '매매처명'] = 'KB'
    df1.loc[df1['매매처명'] == '현대차증권', '매매처명'] = 'HMC'
    df1.loc[df1['매매처명'] == 'NH투자증권', '매매처명'] = 'NH'
    df1.loc[df1['매매처명'] == '미래에셋증권', '매매처명'] = 'Mirae'
    df1.loc[df1['매매처명'] == '맥쿼리(ING)증권', '매매처명'] = 'MACQ'
    df1.loc[df1['매매처명'] == '골드만삭스증권', '매매처명'] = 'GS'
    df1.loc[df1['매매처명'] == '제이피모간증권', '매매처명'] = 'JPM'
    df1.loc[df1['매매처명'] == '유진투자증권', '매매처명'] = 'Eugene'
    df2.loc[df2['매매처'] == '유안타', '매매처'] = 'Yuanta'
    df2.loc[df2['매매처'] == '한투', '매매처'] = 'KIS'

    # '날짜'인덱스의 이름이 일치하지 않으므로 '일자' 인덱스 이름을 변경
    df1 = df1.rename(columns={'일자':'날짜'})
    df1 = df1.rename(columns={'매매처명':'매매처'})
    df2 = df2.rename(columns={'펀드':'펀드코드'})
    df2 = df2.rename(columns={'체결수량':'수량'})
    df2 = df2.rename(columns={'체결단가':'단가'})

    # '매매구분' 칼럼 값 변경
    df1.loc[df1['매매구분'] == '매수', '매매구분'] = 'Buy'
    df1.loc[df1['매매구분'] == '매도', '매매구분'] = 'Sell'

    # '날짜'컬럼의 데이터형식 문제로 인해 통합되지 않는 문제 해결
    df1['날짜'] = pd.to_datetime(df1['날짜'], format='%Y-%m-%d')
    df2['날짜'] = pd.to_datetime(df2['날짜'], format='%Y-%m-%d')

    # 'df1'에 단축코드 컬럼 추가
    df1['단축코드'] = df1['종목코드'].str[3:9]

    df1.loc[df1['단축코드'] == '005382', '단축코드'] = '005387'

    # 'df2'의 주문번호를 문자열로 변환
    df2['주문번호'] = df2['주문번호'].astype(str)

    # 'df2'에 '날짜'와 '주문번호'를 합쳐서 고유코드 생성
    df2['order_id'] = df2['날짜'].astype(str) + '-' + df2['주문번호']

    # 날짜, 종목명, 펀드코드, 매매구분
    merged_df = pd.merge(df1, df2, on=['날짜', '단축코드', '펀드코드', '매매구분', '수량', '매매처', '단가'], how='inner')

    # 중복되는 행 삭제
    merged_df_no_duple = merged_df.drop_duplicates()

    # '날짜', '단축코드', '펀드코드', '매매구분', '수량', '매매처', '단가', 'order_id'가 중복되는 행 삭제
    merged_df_no_duple.drop_duplicates(subset=['날짜', '단축코드', '펀드코드', '매매구분', '수량', '매매처', '단가', 'order_id'], inplace=True)

    # merged_df_no_duple에서 원하는 컬럼을 선택하여 output_df에 저장
    selected_columns = ['날짜', '거래구분', '매매구분', '운용역명', '펀드코드', '펀드명', '단축코드', '종목명_x', '수량', '금액' ,'수수료', '거래세', '매매처', 'order_id']
    output_df = merged_df_no_duple[selected_columns]

    # 변경할 컬럼 이름 딕셔너리 형태로 저장
    new_column_names = {
        '날짜' : 'date',
        '거래구분' : 'SBL',
        '매매구분' : 'tr_direction',
        '운용역명' : 'manager',
        '펀드코드' : 'fund_code',
        '펀드명' : 'fund_name',
        '단축코드' : 'ticker',
        '종목명_x' : 'stock_name',
        '수량' : 'quantity',
        '금액' : 'gross_amount',
        '수수료' : 'commission',
        '거래세' : 'tax',
        '매매처' : 'broker',
        'order_id' : 'order_id'
    }

    # 컬럼 이름 변경
    output_df.rename(columns=new_column_names, inplace=True)

    output_df['date'] = pd.to_datetime(output_df['date']).dt.strftime('%Y-%m-%d')

    # 경로 및 시트이름 설정
    output_file = r'C:\PythonProjects\recon\positions.xlsx'
    sheet_name = 'transaction'

    # 결과를 엑셀 파일로 저장합니다.
    try:
        # 기존 엑셀 파일 열기
        wb = load_workbook(output_file)
        writer = pd.ExcelWriter(output_file, engine='openpyxl')
        writer.book = wb
    except FileNotFoundError:
        # 파일이 없을 경우 새로운 엑셀 파일 생성
        writer = pd.ExcelWriter(output_file, engine='openpyxl')

    output_df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    writer.close()