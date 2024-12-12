import os
import shutil
import openpyxl

def move_files_with_keyword(source_dir, target_dir, keyword):
    # 소스 디렉토리 내의 모든 파일을 검색합니다.
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)

        # 파일 이름에 특정 키워드 포함되어 있으면 이동
        if keyword in filename and not filename.endswith(".pdf"): # 끝에 .txt가 붙은 파일 제외
            target_file = os.path.join(target_dir, filename)

            # 파일 이동
            shutil.move(source_file, target_file)

def rpt_copy(pre_source_dir, pre_dest_dir, rpt_keyword):
    # "EQSWAP16X"를 포함하고 확장자가 .csv인 파일 복사
    try:
        files_copied = 0
        for file_name in os.listdir(pre_source_dir):
            # 파일명에 "EQSWAP16X" 포함 여부와 확장자가 ".xlsx"인지 확인
            if rpt_keyword in file_name and file_name.endswith(".csv"):
                source_file_path = os.path.join(pre_source_dir, file_name)
                if os.path.isfile(source_file_path):  # 파일인지 확인
                    shutil.copy(source_file_path, pre_dest_dir)
                    files_copied += 1
                    print(f"'{file_name}' 파일을 복사했습니다.")
        
        if files_copied == 0:
            print("복사할 파일이 없습니다.")
        else:
            print(f"총 {files_copied}개의 파일이 성공적으로 복사되었습니다.")
    except Exception as e:
        print(f"파일 복사 중 오류가 발생했습니다: {e}")

def rpt_move(pre_source_dir, pre_dest_dir, rpt_keyword):
    # "EQSWAP16X"를 포함하고 확장자가 .csv인 파일 복사
    try:
        files_moved = 0
        for file_name in os.listdir(pre_source_dir):
            # 파일명에 "EQSWAP16X" 포함 여부와 확장자가 ".xlsx"인지 확인
            if rpt_keyword in file_name and file_name.endswith(".csv"):
                source_file_path = os.path.join(pre_source_dir, file_name)
                if os.path.isfile(source_file_path):  # 파일인지 확인
                    shutil.move(source_file_path, pre_dest_dir)
                    files_moved += 1
                    print(f"'{file_name}' 파일을 이동됐습니다.")
        
        if files_moved == 0:
            print("이동시킬 파일이 없습니다.")
        else:
            print(f"총 {files_moved}개의 파일이 성공적으로 이동되었습니다.")
    except Exception as e:
        print(f"파일 복사 중 오류가 발생했습니다: {e}")


def main():
    source_dir = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP"
    target_dir = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP/opening"
    keyword = "New_Trade"  # 검색할 단어 입력

    move_files_with_keyword(source_dir, target_dir, keyword)


    source_dir2 = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP"
    target_dir2 = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP/closing"
    keyword2 = "Unwind_Trade"  # 검색할 단어 입력

    move_files_with_keyword(source_dir2, target_dir2, keyword2)


    source_dir3 = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP"
    target_dir3 = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP/position"
    keyword3 = "Daily_P&L_"  # 검색할 단어 입력

    move_files_with_keyword(source_dir3, target_dir3, keyword3)


    source_dir4 = r"Z:/02.펀드/003.매매보고서 대사/KIS-SWAP"
    target_dir4 = r"Z:/02.펀드/003.매매보고서 대사/KIS-SWAP/opening"
    keyword4 = "New Trade"  # 검색할 단어 입력

    move_files_with_keyword(source_dir4, target_dir4, keyword4)


    source_dir5 = r"Z:/02.펀드/003.매매보고서 대사/KIS-SWAP"
    target_dir5 = r"Z:/02.펀드/003.매매보고서 대사/KIS-SWAP/closing"
    keyword5 = "Termination"  # 검색할 단어 입력

    move_files_with_keyword(source_dir5, target_dir5, keyword5)


    source_dir6 = r"Z:/02.펀드/003.매매보고서 대사/KIS-SWAP"
    target_dir6 = r"Z:/02.펀드/003.매매보고서 대사/KIS-SWAP/position"
    keyword6 = "Open Position"  # 검색할 단어 입력

    move_files_with_keyword(source_dir6, target_dir6, keyword6)


    source_dir7 = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP"
    target_dir7 = r"Z:/02.펀드/003.매매보고서 대사/KB-SWAP/collateral"
    keyword7 = "Collateral Summary"  # 검색할 단어 입력

    move_files_with_keyword(source_dir7, target_dir7, keyword7)

    # 원본, 목표 디렉터리 설정
    pre_source_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM"
    pre_es16_dest_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM/ES16"
    rpt16_keyword = "EQSWAP16X"

    pre_es24_dest_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM/ES24"
    rpt24_keyword = "EQSWAP24MX"

    pre_es40_dest_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM/ES40"
    rpt40_keyword = "EQSWAP40X"

    rpt_copy(pre_source_dir, pre_es16_dest_dir, rpt16_keyword)
    rpt_copy(pre_source_dir, pre_es24_dest_dir, rpt24_keyword)
    rpt_copy(pre_source_dir, pre_es40_dest_dir, rpt40_keyword)


    pre_source_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM"
    pre_dest_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM/old"
    keywords = ["EQSWAP16", "EQSWAP16X", "EQSWAP24M", "EQSWAP24MX", "EQSWAP40", "EQSWAP40X"]

    try:
        files_moved = 0
        for file_name in os.listdir(pre_source_dir):
            # 파일명에서 키워드 확인
            for keyword in keywords:
                if file_name.startswith(keyword):  # 키워드로 시작하는 파일인지 확인
                    source_file_path = os.path.join(pre_source_dir, file_name)
                    if os.path.isfile(source_file_path):  # 파일인지 확인
                        shutil.move(source_file_path, pre_dest_dir)
                        files_moved += 1
                        print(f"'{file_name}' 파일을 이동했습니다.")
                    break  # 키워드 매칭이 되었으면 더 이상 확인하지 않음
        
        if files_moved == 0:
            print("이동할 파일이 없습니다.")
        else:
            print(f"총 {files_moved}개의 파일이 성공적으로 이동되었습니다.")
    except Exception as e:
        print(f"파일 이동 중 오류가 발생했습니다: {e}")

    
    
    print("Files moved successfully.")

if __name__ == "__main__":
    main()