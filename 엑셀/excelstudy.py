import openpyxl
import os
import pyexcel as p
import pandas as pd

#파일들의 제목 찾아서 리스트에 저장
def path_set():
    files = os.listdir('.')
    excel_files=set()
    for file in files:
        if file[-8:] == 'dark.xls':
            excel_files.add(file[:-8])
        if file[-9:] == 'light.xls':
            excel_files.add(file[:-9])
    #파일 순서대로 정렬
    return sorted(list(excel_files))


def light_dark(path):
    #경로 설정
    path_light = path + 'light.xls'
    path_dark = path + 'dark.xls'

    #엑셀파일
    light=pd.read_excel(path_light, usecols=[0])
    dark =pd.read_excel(path_dark, usecols=[0])
    answer = light -dark
    answer = answer.rename(columns={'DrainI':path})
    return answer


excel_files = path_set()
answer_list = pd.DataFrame([i for i in range(1,101)])
for excel_file in excel_files:
    temp = light_dark(excel_file)
    answer_list = answer_list.join(temp)


answer_list.to_excel('준환짱.xlsx')
