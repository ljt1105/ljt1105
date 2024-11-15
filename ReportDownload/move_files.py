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

def move_files_with_keyword2(source_dir, target_dir, keyword):
    # 소스 디렉토리 내의 모든 파일을 검색합니다.
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
 
        # 파일 이름에 특정 키워드 포함되어 있으면 이동
        if keyword in filename and "Summary" not in filename: # 끝에 .txt가 붙은 파일 제외
            target_file = os.path.join(target_dir, filename)

            # 파일 이동
            shutil.move(source_file, target_file)

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

    move_files_with_keyword2(source_dir3, target_dir3, keyword3)


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
    pre_es16_source_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM"
    pre_es16_dest_dir = r"Z:/02.펀드/003.매매보고서 대사/PRELUDE_MTM/ES16"

    # "EQSWAP16X"를 포함하고 확장자가 .xlsx인 파일 복사
    try:
        files_copied = 0
        for file_name in os.listdir(pre_es16_source_dir):
            # 파일명에 "EQSWAP16X" 포함 여부와 확장자가 ".xlsx"인지 확인
            if "EQSWAP16X" in file_name and file_name.endswith(".xlsx"):
                source_file_path = os.path.join(pre_es16_source_dir, file_name)
                if os.path.isfile(source_file_path):  # 파일인지 확인
                    shutil.copy(source_file_path, pre_es16_dest_dir)
                    files_copied += 1
                    print(f"'{file_name}' 파일을 복사했습니다.")
        
        if files_copied == 0:
            print("복사할 파일이 없습니다.")
        else:
            print(f"총 {files_copied}개의 파일이 성공적으로 복사되었습니다.")
    except Exception as e:
        print(f"파일 복사 중 오류가 발생했습니다: {e}")


    print("Files moved successfully.")

if __name__ == "__main__":
    main()