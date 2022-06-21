'''
설정 파일을 관리하는 모듈입니다.
'''
import configparser
### 메인 창 모듈의 AutoGetServiceDay이 작동될 시각을 정합니다.
NextLaunchHour = 5 #휴일 정보를 받아올 시각 (24시간)

 #설정 파일명 설정
FileName = 'Settings.ini'

#설정 파일 내부 설정
SectionName = 'Settings'
SectionName2 = 'DatabaseUpdateDate'
SectionName3 = 'DatabaseFileName'

#어느 모듈에서도 설정 값을 가져올 수 있는 MagicWord 설정
MagicWord_Line = 'line'
MagicWord_Station = 'station'
MagicWord_Line1_DB = 'line1'
MagicWord_Line2_DB = 'line2'
MagicWord_Line3_DB = 'line3'

#호선별 SWITCH_CASE문을 사용하기 위한 딕셔너리 자료형입니다.
SETDBDATE_CASE = {1:MagicWord_Line1_DB,
               2:MagicWord_Line2_DB,
               3:MagicWord_Line3_DB }

ConfigStyle = configparser.ConfigParser()

ConfigStyle[SectionName] = {
    MagicWord_Line: '2',
    MagicWord_Station: '용산' }

ConfigStyle[SectionName2] = {
    MagicWord_Line1_DB: '',
    MagicWord_Line2_DB: '',
    MagicWord_Line3_DB: '' }

ConfigStyle[SectionName3] = {
    MagicWord_Line1_DB: '',
    MagicWord_Line2_DB: '',
    MagicWord_Line3_DB: '' }



### 설정 파일 읽기
config = configparser.ConfigParser()
dataset = config.read(FileName)

### 메인 부분 파일이 존재하지 않을 때 설정 파일 생성
if FileName not in dataset :
    config = ConfigStyle
    '''
    config[SectionName] = ConfigStyle[SectionName]
    config[SectionName2] = ConfigStyle[SectionName2]
    config[SectionName2] = ConfigStyle[SectionName2]
    '''
    with open(f'./{FileName}', 'w') as file:
        config.write(file)


def StationLoad() :
    '''
    사용자의 호선 및 역 설정 값을 불러들이는 함수입니다.
    '''
    return dict(config[SectionName])
    

def StationSave(line = 2, station = "용산") :
    '''
    사용자의 호선 및 역 설정 값을 저장하는 함수입니다.
    '''
    config[SectionName][MagicWord_Line] = str(line)
    config[SectionName][MagicWord_Station] = station
    with open(f'./{FileName}', 'w') as f:
        config.write(f)

    
def DatabaseInfoLoad():
    '''
    저장된 시간표 파일의 정보에 관한 정보를 불러들이는 함수입니다.
    '''
    return dict(config[SectionName2])

def DatabaseFileNameLoad(line = 2):
    '''
    저장된 시간표 파일의 정보를 불러들이는 함수입니다.
    '''
    return config[SectionName3][SETDBDATE_CASE[line]]
    

def DatabaseInfoSave(line = 2, date = "", filename=""):
    '''
    저장한 시간표 파일의 정보를 설정파일에 기록하는 함수입니다.
    '''
    config[SectionName2][SETDBDATE_CASE[line]] = date
    config[SectionName3][SETDBDATE_CASE[line]] = filename
    
    with open(f'./{FileName}', 'w') as file:
        config.write(file)

def GetLineTotal():
    '''
    몇 호선이 기록되어 있는지 알아내기 위한 함수
    '''
    return list(SETDBDATE_CASE.keys())
                
