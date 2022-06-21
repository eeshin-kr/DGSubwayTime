'''
시간표(Database)를 외부 사이트에서 가져오기 위한 함수입니다.
'''
from urllib import request
from urllib import error
import json
from Processing import SettingsManager

#호선별 시간표 정보 JSON 다운로드 주소입니다.
Line1 = "https://www.data.go.kr/catalog/15065526/fileData.json"
Line2 = "https://www.data.go.kr/catalog/3033376/fileData.json"
Line3 = "https://www.data.go.kr/catalog/15065532/fileData.json"
#SWITCH_CASE문 처럼 사용하기 위한 딕셔너리 변수입니다.
JSON_CASE = {1: Line1,
            2: Line2,
            3: Line3}



def GetDBD(LineNum = 2):
    '''
    시간표(Database)의 최신 수정일자(Date)를 받아오기 위한 함수입니다.
    '''
    try:
        jsonURL = JSON_CASE[LineNum]
        jsonURLOpen = request.urlopen(url=jsonURL)
        jsonURLData = jsonURLOpen.read()
        Encoding = jsonURLOpen.info().get_content_charset()
        jsonData = json.loads(jsonURLData.decode(Encoding))
        LastModified = jsonData['dateModified']

        return LastModified
    except TimeoutError as e:
        print("타임아웃 에러 발생")
        return -1
        



def DownloadFromJson(LineNum = 2):
    '''
    JSON 파일로 부터 시간표 파일을 받아오기 위한 함수입니다.
    '''
    jsonURL = JSON_CASE[LineNum]
    
    jsonURLOpen = request.urlopen(url=jsonURL)
    jsonURLData = jsonURLOpen.read()
    Encoding = jsonURLOpen.info().get_content_charset()
    jsonData = json.loads(jsonURLData.decode(Encoding))

    DistributionData = jsonData['distribution']
    DistributionDict = dict(DistributionData[0])
    CSVDownloadURL = DistributionDict['contentUrl']
    print("다운로드 중")
    CSVDownloadOpen = request.urlopen(url=CSVDownloadURL)
    CSVDownloadData = CSVDownloadOpen.read()
    if LineNum == 2 :
        CSVDownloadData = CSVFix(CSVDownloadData)
    #파일 이름 가져오기
    CSVDownloadName_raw = CSVDownloadOpen.headers.get_filename()
    CSVDownloadName = CSVDownloadName_raw.encode('ISO-8859-1').decode('utf-8') #파일 이름이 ISO-8859-1로 인코딩 되어 있음...
    print("다운로드 완료")
    #파일 저장하기
    with open(f'./{CSVDownloadName}', mode="wb") as file:
        file.write(CSVDownloadData)
    #설정파일에 파일 수정일 및 파일명 저장
    SettingsManager.DatabaseInfoSave(line = LineNum, date = GetDBD(LineNum), filename=CSVDownloadName)
    
    
##2호선에 신매역이 신내역으로 기록, 이름 수정함
def CSVFix(CSV_Byte):
    '''
    외부의 CSV 파일에 문제가 있을 경우 CSV파일을 수정하기 위해 사용하는 함수입니다.
    '''
    CSV_Byte = CSV_Byte.decode('euc-kr')
    CSV_Byte = CSV_Byte.replace("신내","신매") #2호선 파일에 신매역이 신내역으로 기록되어 있음
    return CSV_Byte.encode('euc-kr')

def isUpdateAvailable(LineNum = 2):
    '''
    설정 파일의 수정일과 외부 파일의 수정일을 비교하여 업데이트가 필요한지 확인하는 함수입니다.
    '''
    LastDBD = GetDBD(LineNum)
    SavedDBD = SettingsManager.DatabaseInfoLoad()[SettingsManager.SETDBDATE_CASE[LineNum]]
    if LastDBD == -1 :
        return -1
    elif LastDBD != SavedDBD :
        return [SavedDBD, LastDBD]
    else:
        return False
    


