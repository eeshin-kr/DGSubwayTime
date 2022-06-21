'''
시간표 CSV파일을 읽어오고 처리하기 위한 모듈입니다.
'''
import csv
import time
import tkinter.messagebox
from Processing import SettingsManager
from Processing import DownloadSchedule



##초기 실행 함수 시간표 CSV 파일의 최신버전 여부 확인
def CheckUpdate(Line):
    UpdateCheck = DownloadSchedule.isUpdateAvailable(Line)
    
    if UpdateCheck == -1 :
        pass
    elif UpdateCheck :
        if tkinter.messagebox.askyesno(title="열차 시간표 알리미", message=f'''{Line}호선 시간표 업데이트가 존재합니다. 다운로드 하시겠습니까?
 현재 버전: {UpdateCheck[0]} 최신 버전: {UpdateCheck[1]}'''):
            DownloadSchedule.DownloadFromJson(Line)
            LoadCSV(Line)
def LoadCSV(Line):
    ###CSV 파일 불러와서 timetable_list 변수에 저장
    global timetable_list
    
    try:
        CSVFileName = SettingsManager.DatabaseFileNameLoad(Line)
        with open(CSVFileName, 'r', encoding='euc-kr') as timetable_csv: 
            timetable_list = list(csv.reader(timetable_csv))
    except FileNotFoundError:
        if tkinter.messagebox.askyesno(title="열차 시간표 알리미", message=f'{Line}호선 시간표 파일을 찾을 수 없습니다. 다운로드 하시겠습니까?', icon = 'warning'):
            DownloadSchedule.DownloadFromJson(Line)
            CSVFileName = SettingsManager.DatabaseFileNameLoad(Line)
        with open(CSVFileName, 'r', encoding='euc-kr') as timetable_csv: 
            timetable_list = list(csv.reader(timetable_csv))
    
##모듈을 불러올 때 초기 CSV파일을 읽고 업데이트를 확인합니다.
LoadCSV(int(SettingsManager.StationLoad()[SettingsManager.MagicWord_Line]))
CheckUpdate(int(SettingsManager.StationLoad()[SettingsManager.MagicWord_Line]))
##########

def tstrlist2int(strlist):
    '''
    시간 str을 int로 변환하는 함수
    '''
    try:
        intlist = list(map(int,strlist))
        return intlist[0]*3600+intlist[1]*60+intlist[2]
    except ValueError:
        return -1


##열차 시각과 남은 시간 출력하는 불러오는 함수
def TimeTableSearchT(week="평일",
                    direction="상", station="용산",
                    adtype="도착", SearchTime=''):
    
    tlist = timetable_list
    StationList = GetStationList()
    if station == StationList[-1] and direction == "상" and adtype =="도착": ##시점에서는 도착이 없음
        adtype="출발"
    elif station == StationList[0] and direction == "하" and adtype == "도착":
        adtype="출발"
    elif station == StationList[-1] and direction == "하" and adtype == "출발": ##종점에서는 출발이 없음
        adtype="도착"
    elif station == StationList[0] and direction =="상" and adtype == "출발":
        adtype="도착"
    
    SearchTInt = tstrlist2int(SearchTime.split(':'))
    
    for line in tlist:
        if (week      in line[0] and
            direction in line[0] and
            station   in line    and
            adtype    in line):
        
            for colline in line:
                if(":" in colline):                    
                    timetableinfo = tstrlist2int(colline.split(":"))
                    if SearchTInt < timetableinfo:
                        return colline
                    
            for colline in line: ##이후의 시간 대에 편성 없을 경우 예외 경우로 사용
                if(":" in colline):
                    #timetableinfo = tstrlist2int(colline.split(":"))
                    #nowtdiff = timetableinfo + (24*3600) - SearchTInt
                    return colline   
             
    raise NameError('시간표를 검색하는데 실패했습니다. 마지막 선택 역:' + station)

##열차 시각과 남은시각, 다음 열차 출력하는 함수
def TimeTableSearch(week="평일",
                    direction="상", station="용산",
                    adtype="도착", SearchTime=""):
    
    NowTime = time.strftime("%H:%M:%S")
    NowTrain  = TimeTableSearchT(week, direction, station, adtype, SearchTime = NowTime)
    NextTrain = TimeTableSearchT(week, direction, station, adtype, SearchTime = NowTrain)
    return [NowTrain,NextTrain]

def GetStationList(week="평일", direction="하",HdColWord="요일별" ,StColWord="역명") :

    tlist = timetable_list
    HolidayCol = 0
    StationCol = 0
    StationList = []

    for col in tlist[0]: ##요일별이 몇 열에 있는지 확인
        if HdColWord in col :
            break
        HolidayCol = HolidayCol + 1
    
    for col in tlist[0]: ##역명이 몇 열에 있는지 확인
        if StColWord in col :
            break
        StationCol = StationCol + 1

    if HolidayCol >= 50  or StationCol >= 50 :
        raise NameError('휴일이나 역명 칼럼을 확인할 수 없습니다.')
    
    for line in tlist[1:-1]:
        if (week in line[HolidayCol] and
            direction in line[HolidayCol]) :
            if line[StationCol] not in StationList:
                StationList.append(line[StationCol])
    return StationList
            
#현재 시간과 지정된 시간의 차이를 불러오는 함수
def TimeDiffInt(TimeStr):
    TimeNowInt = tstrlist2int(time.strftime("%H:%M:%S").split(':'))
    TimeDesInt = tstrlist2int(TimeStr.split(":"))
    if TimeNowInt > TimeDesInt:
        return 24*3600 - TimeNowInt + TimeDesInt
    else:
        return TimeDesInt - TimeNowInt

#해당 역사의 상/하선 별 시간표를 리스트로 반환하는 함수
def GetTimeTable(week="평일", direction="상", station="용산", adtype="도착"):
    
    tlist = timetable_list
    StationList = GetStationList()
    if station == StationList[-1] and direction == "상" and adtype =="도착": ##시점에서는 도착이 없음
        adtype="출발"
    elif station == StationList[0] and direction == "하" and adtype == "도착":
        adtype="출발"
    elif station == StationList[-1] and direction == "하" and adtype == "출발": ##종점에서는 출발이 없음
        adtype="도착"
    elif station == StationList[0] and direction =="상" and adtype == "출발":
        adtype="도착"

    TempList = []
    
    for row in tlist :
        if (week in row[0] and
            direction in row[0] and
            station in row and
            adtype in row):

            for col in row :
                if ":" in col :
                    TempList.append(col)
            return TempList

    print("CSV 파일로 부터 시간표 정보를 받아오지 못했습니다.")
    return TempList


def GetTimeTable2 (week="평일", direction="상", adtype="도착"):
    '''
    열차별 시간표의 트리뷰에 사용하기위한 함수입니다.
    열차별 시간을 모두 가져옵니다.
    '''
    tlist = timetable_list
    StationList = GetStationList()
    CurrentStationIndex = None
    TrainNumDict = {}
    TrainNumIndexDict = {}
    EmptyList = [ None for a in range(len(StationList))] #역사 갯수 만큼의 None이 든 리스트
    SkipList = [ None for a in range(len(StationList))] #출발, 도착을 했는지 기록하는 리스트

    for Temp in tlist[0] :
        if (Temp[-4:].isnumeric()) == True:
            TrainNumDict[Temp[-4:]] = EmptyList #열차 번호 - 시간대 리스트 저장
            TrainNumIndexDict[tlist[0].index(Temp)] = Temp[-4:] #인덱스 번호 - 열차 번호쌍 저장

    for row in tlist :
        if (week in row[0] and
            direction in row[0]):

            for col in row:
                if col in StationList :
                    ##현재 검색중인 역사의 인덱스 번호 계산
                    CurrentStationIndex = StationList.index(col)
                    break
                
                
            for col in row :
                
                if SkipList[CurrentStationIndex] == True : ##종점 및 시점에서의 출발/도착 예외처리를 위함, 도착으로 작성되어 있으면 해당 역사는 건너뜀
                        break
                    
                ##Dictionary에 열차 시간 기록
                if ":" in col: #딕셔너리 타입을 다룰 때에는 copy 주의

                    a = TrainNumIndexDict[row.index(col)]
                    tmp = list(TrainNumDict[a]) ##list형으로 변환하여 값 복사
                    tmp[CurrentStationIndex] = col
                    TrainNumDict[a] = tmp

            if adtype in row:
                SkipList[CurrentStationIndex] = True
                

                

    for (key, val) in list(TrainNumDict.items()) : #시간이 기록되지 않는 없는 열차번호 제거
        if val == EmptyList : del TrainNumDict[key]

    return TrainNumDict

       
def GetHolidayOptionList(): ##추후 휴일 옵션 항목 가져오는 함수 만들 예정
    pass

def ChangeLine(Line):
    '''
    호선이 바뀌었을 때 CSV파일을 다시 불러오기 위한 함수입니다.
    '''
    LoadCSV(Line)
    #CheckUpdate(Line)

    
