# trade팀에서 받은 거래내역을 하나의 파일로 통합하는 코드

import os
import pandas as pd
from datetime import datetime

def integrating_transaction_history():

    # 파일들이 있는 경로 지정
    folder_path = r'C:\PythonProjects\recon\거래내역'
    result_df_path = r'C:\PythonProjects\recon'

    # 경로에 있는 파일들의 목록 가져오기
    file_list = os.listdir(folder_path)

    # 엑셀 파일만 필터링
    excel_files = [file for file in file_list if file.endswith('.xlsx')]

    # 모든 엑셀 파일을 하나의 데이터프레임으로 통합
    dfs = []
    for file in excel_files:
        file_path = os.path.join(folder_path, file)

        # 첫 번째 행을 인덱스로 사용
        df = pd.read_excel(file_path, header=0)

        # 파일명에서 날짜 추출
        file_date = file.split()[0]  # 파일명에서 첫 번째 단어(날짜 부분) 추출
        file_date = file_date.replace('월', '-').replace('일', '')  # '월'과 '일'을 '-'로 변경
        file_date = '2024-' + file_date

        print(file_date)

        # '펀드' 칼럼 값이 변경
        df.loc[df['펀드'] == '하이일드', '펀드'] = 'DM11001'
        df.loc[df['펀드'] == '공모주1호', '펀드'] = 'DM12001'
        df.loc[df['펀드'] == '공모주2호', '펀드'] = 'DM12002'
        df.loc[df['펀드'] == '포커스', '펀드'] = 'DM12003'
        df.loc[df['펀드'] == '알파', '펀드'] = 'DM12007'
        df.loc[df['펀드'] == '코스닥벤처', '펀드'] = 'DM13001'
        df.loc[df['펀드'] == '멀티전략', '펀드'] = 'DM14001'

        # '매매구분' 칼럼 값 변경
        df.loc[df['매매구분'] == 'Buy cover', '매매구분'] = 'Buy'
        df.loc[df['매매구분'] == 'Sell short', '매매구분'] = 'Sell'
        
        # 4번째 열(column) 선택 후 문자열로 변환하여 저장
        df.iloc[:, 2] = df.iloc[:, 2].apply(lambda x: str(x).zfill(6))
        
        try:
            # 날짜 형식 변경 시도
            file_date = pd.to_datetime(file_date, format='%Y-%m-%d').strftime('%Y-%m-%d')
            
            # 날짜가 유효한지 검증
            datetime.strptime(file_date, '%Y-%m-%d')
        except ValueError:
            # 유효하지 않은 날짜이면 건너뛰고 다음 파일 처리
            print(f"파일 '{file}'에서 유효하지 않은 날짜를 발견하여 해당 파일을 건너뜁니다.")
            continue
        
        # 데이터프레임에 날짜 열 추가
        df['날짜'] = file_date

        # 11번째 열에 있는 데이터를 첫 번째 행으로 옮기기
        df = df.reindex(['날짜', '펀드', '매매처', '단축코드', '종목명', '운용역명', '매매구분', '체결수량', '체결단가', '체결금액', '주문번호'], axis = 1)

        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)

    change_stock_name(merged_df,'오션브릿지', '티이엠씨씨엔에스')
    change_stock_name(merged_df, '레고켐바이오', '리가켐바이오')

    # 통합된 데이터프레임을 엑셀 파일로 저장
    output_file = os.path.join(result_df_path, 'result_df.xlsx')
    merged_df.to_excel(output_file, index=False)

    print("통합된 데이터프레임이 저장되었습니다.")

def change_stock_name(df, former, now):
    df.loc[df['종목명'] == former, '종목명'] = now