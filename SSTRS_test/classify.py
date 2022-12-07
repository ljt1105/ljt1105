# File Move

import os
import shutil

# Read file name and Listing classification part
def fileList(path_before : str)->list :
    file_list = os.listdir(path_before) #Listing file name list
    category = [] #Make empty list to save file name list
    for file in file_list:
        temp_list = file.split("_") #Separate the file names with "_" and list them
        category.append(temp_list[0]) #리스트의 -2 인덱싱 데이터를 category에 추가

    temp_set = set(category) #중복을 제거하기 위해 set 사용
    result = list(temp_set) #중복 제거 후 다시 리스트화
    return result #결과 리턴


#죄 분류 리스트를 받아와서 정해진 위치에 폴더 생성
def makeFolder(path_after : str, file_list : list):    
    #폴더가 이미 생성되어있다면 오류가 발생하므로 예외처리 진행
    for file in file_list:
        try:
            os.makedirs(path_after+"/"+file)
        except:
            pass

#파일을 폴더 분류에 맞게 이동
def moveFile(path_before, path_after):
    folderlist = os.listdir(path_after)
    filelist = os.listdir(path_before)
    dict = {}

    #파일명에 대한 폴더명을 딕셔너리로 저장
    for file in filelist:
        temp_list = file.split("_")
        dict[file]=temp_list[0]
    
    #딕셔너리 정보 활용하여 파일 이동
    for key, value in dict.items():
        # shutil.move(path_before+"/"+key, path_after+"/"+value)
        try:
            shutil.move(path_before+"/"+key, path_after+"/"+value)
        except:
            pass
    
    
# if __name__ == "__main__" :
def classify_files():
    #분류할 파일이 있는 위치 폴더
    path_before = r"Z:\03.고유\001.Ops\삼성증권 TRS01 거래\07. Test"
    file_list = fileList(path_before)

    #옮길 경로 폴더
    path_after = r"Z:\03.고유\001.Ops\삼성증권 TRS01 거래\07. Test"
    makeFolder(path_after, file_list)
    moveFile(path_before, path_after)