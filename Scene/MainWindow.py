'''
메인 창을 나타내는 모듈입니다.
'''
import webbrowser
import tkinter as tk
from tkinter import ttk
from Processing import csvread
from Processing import todayService
from Processing import SettingsManager
from Processing import DownloadSchedule
from Scene import HelpWindow
from Scene import TimeTableWindow

##################
#열차 시간 알리미 메인화면
#만든이: realoven@gmail.com
##################

'''
휴일 정보를 받아오기 위한 변수입니다. SettingsManager에 설정된 시간을 받아옵니다.
'''
NextHolidayGetHour = SettingsManager.NextLaunchHour #휴일 정보를 받아올 시각 (24시간 기준)

def RefreshTime():
    '''
    지정된 시간 마다 선택된 역의 이번 열차와 다음 열차의 시간을 가져오고 현재 시간과 비교하는 함수입니다.
    '''
    TmpList = csvread.TimeTableSearch(direction="상", station=StationSelection, week=HolidaySelection)
    TmpList2 = csvread.TimeTableSearch(direction="하",  station=StationSelection, week=HolidaySelection)
    
    CurrentTrainUP = TmpList[0]
    CurrentTrainElapsedUP = csvread.TimeDiffInt(TmpList[0])
    
    NextTrainUP = TmpList[1]
    NextTrainElapsedUP = csvread.TimeDiffInt(TmpList[1])

    CurrentTrainDOWN = TmpList2[0]
    CurrentTrainElapsedDOWN = csvread.TimeDiffInt(TmpList2[0])
    NextTrainDOWN = TmpList2[1]
    NextTrainElapsedDOWN = csvread.TimeDiffInt(TmpList2[1])
    
    '''
    메인 창에 시간표 정보를 나타내기 위한 함수입니다.
    isLastTrain 함수를 통해 해당 시간이 막차인지 확인하고 글자를 지정된 색상으로 변경합니다.
    '''

    
    Tstr1.set(CurrentTrainUP[:-3]) #초는 제외하고 표시
    Tstr3.set(NextTrainUP[:-3])
    
    
    if csvread.isLastTrain(direction="상", station=StationSelection, week=HolidaySelection, Time=TmpList[0]) :
        LastDestination1 = csvread.GetDestination(week=HolidaySelection, direction="상", station = StationSelection)
        Tstr0.set(f'{TimeElapseString(CurrentTrainElapsedUP)} \n({LastDestination1}행)')
        TLabelTOPU0.configure(fg="red")
        TLabelTOPD0.configure(fg="red")
        
    else:
        Tstr0.set(TimeElapseString(CurrentTrainElapsedUP))
        TLabelTOPU0.configure(fg="black")
        TLabelTOPD0.configure(fg="black")

    if csvread.isLastTrain(direction="상", station=StationSelection, week=HolidaySelection, Time=TmpList[1]):
        LastDestination2 = csvread.GetDestination(week=HolidaySelection, direction="상", station = StationSelection)
        Tstr2.set(f'{TimeElapseString(NextTrainElapsedUP)} \n({LastDestination2}행)')
        TLabelTOPU1.configure(fg="red")
        TLabelTOPD1.configure(fg="red")
        
    else:
        Tstr2.set(TimeElapseString(NextTrainElapsedUP))
        TLabelTOPU1.configure(fg="black")
        TLabelTOPD1.configure(fg="black")
        

    Tstr5.set(CurrentTrainDOWN[:-3]) #초는 제외하고 표시
    Tstr7.set(NextTrainDOWN[:-3])
    

    if csvread.isLastTrain(direction="하", station=StationSelection, week=HolidaySelection, Time=TmpList2[0]):
        LastDestination3 = csvread.GetDestination(week=HolidaySelection, direction="하", station = StationSelection)
        Tstr4.set(f'{TimeElapseString(CurrentTrainElapsedDOWN)} \n({LastDestination3}행)')
        TLabelBOTU0.configure(fg="red")
        TLabelBOTD0.configure(fg="red")
    else:
        Tstr4.set(TimeElapseString(CurrentTrainElapsedDOWN))
        TLabelBOTU0.configure(fg="black")
        TLabelBOTD0.configure(fg="black")

    if csvread.isLastTrain(direction="하", station=StationSelection, week=HolidaySelection, Time=TmpList2[1]):
        LastDestination4 = csvread.GetDestination(week=HolidaySelection, direction="하", station = StationSelection)
        Tstr6.set(f'{TimeElapseString(NextTrainElapsedDOWN)} \n({LastDestination4}행)')        
        TLabelBOTU1.configure(fg="red")
        TLabelBOTD1.configure(fg="red")
    else:
        Tstr6.set(TimeElapseString(NextTrainElapsedDOWN))
        TLabelBOTU1.configure(fg="black")
        TLabelBOTD1.configure(fg="black")
        

    

    UpdateFrameLabel() #라벨 업데이트 포함
    win.after(1000, RefreshTime)

def AutoGetServiceDay():
    '''
    휴일 여부를 받아오는 함수입니다.
    '''
    global HolidaySelection
    global HolidayRadioOption
    global HolidayOptionList
    
    todayServiceStr = todayService.GetTodayServiceDayNaver()
    if todayServiceStr in HolidayOptionList:
        HolidayRadioOption.set(todayServiceStr)
        HolidaySelection = HolidayRadioOption.get()
    else :
        print("네이버 지도로 부터 올바른 휴일 정보를 받지 못하였습니다." + todayServiceStr)

    # 다시 실행 구문 시험하지는 않음
    # 지금 시각과 24:00 사이의 초를 계산, 그 후 지정된 시간 만큼 초 더한 뒤 Millsec으로 변환
    NextLaunchTime = (csvread.TimeDiffInt("24:00:00")+NextHolidayGetHour*3600) * 1000
    win.after(NextLaunchTime, AutoGetServiceDay)

def TimeElapseString(ElapsedTime):
    '''
    RefreshTime에서 현재시관과의 차는 초로 계산되는데 이를 읽기 쉽게 시간, 분, 초로 바꿔주는 함수입니다.
    '''
    if ElapsedTime//60 >= 60:
        return f'{ElapsedTime//3600} 시간 {ElapsedTime%3600//60}분 {ElapsedTime%60}초'
    else:
        return f'{ElapsedTime//60}분 {ElapsedTime%60}초'

def ChangeLine(LineInt):
    '''
    메뉴에서 호선을 바꿀때 동작하는 함수입니다.
    LineSelection 변수 값을 바꾸고, 시간표 데이터를 다시 불러오고 역 설정 메뉴의 값을 새로고침 합니다.
    '''
    global LineSelection
    global StationList
    global StationSelection
    
    LineSelection = LineInt
    csvread.ChangeLine(LineInt)
    StationList = csvread.GetStationList()
    StationSelection = StationList[7]
    UpdateStationMenu()
    

def ChangeStation(StationStr):
    '''
    메뉴를 통해 역을 바꾸었을때 동작하는 함수입니다.
    '''
    global StationSelection
    StationSelection = StationStr

def ChangeHoliday(HolidayStr):
    '''
    메뉴를 통해 휴일 여부를 바꾸었을때 동작하는 함수입니다.
    '''
    global HolidaySelection
    HolidaySelection = HolidayStr
    
def UpdateFrameLabel():
    '''
    메인 화면의 역 이름, 방면 명을 새로고침하기 위한 함수입니다.
    '''
    MFrame.configure(text=f'{StationSelection} / {HolidaySelection}')
    SFrameTOP.configure(text=f'{StationList[0]} 방면')
    SFrameBOT.configure(text=f'{StationList[-1]} 방면')


def UpdateStationMenu():
    '''
    호선을 바꾸었을 때 메인화면 역 설정 메뉴의 값을 해당 호선에 맞게 변경하기위한 함수입니다.
    '''
    menu_station.delete(0, 'end')
    
    for StationOption in StationList:
      menu_station.add_radiobutton(label=StationOption, variable=StationRadioOption, value = StationOption, command=lambda: ChangeStation(StationRadioOption.get()))

    StationRadioOption.set(StationSelection)    

def ToggleLabelVisibility():
    if len(TFrameTOP0.pack_slaves()) > 1:
        TLabelTOPD0.pack_forget()
        TLabelTOPD1.pack_forget()
        TLabelBOTD0.pack_forget()
        TLabelBOTD1.pack_forget()
    else:
        TLabelTOPD0.pack()
        TLabelTOPD1.pack()
        TLabelBOTD0.pack()
        TLabelBOTD1.pack()
    

def StartUpMain():
    '''
    초기 시작 시 메인 화면의 새로고침 및 메뉴를 작동시키기 위한 함수입니다.
    휴일 설정, 역사 남은 시간을 계산하는 함수와 메인창을 업데이트하기 위한 함수를 실행합니다.
    '''
    AutoGetServiceDay()
    RefreshTime()
    win.mainloop()

'''
메인 화면의 위치를 정하는 변수입니다.
'''
#default_x = 300
#default_y = 200
default_x_po = 20
default_y_po = 40

'''
메인 화면의 인터페이스에 사용할 변수입니다.
LineList: SettingsManager에 기록된 호선 목록을 받아옵니다.
StationList: csv파일에 기록된 호선의 역사 목록을 불러옵니다.
HolidayOptionList: 휴일 목록입니다.
LineSelection: 사용자가 선택한 호선을 나타냅니다. 초기에는 SettingsManager를 통해 마지막 선택 값을 불러옵니다.
StationSelection: 사용자가 선택한 역을 나타냅니다. 초기에는 SettingsManager를 통해 마지막 선택 값을 불러옵니다.
HolidaySelection: 사용자가 선택한 휴일을 나타냅니다. 초기 설정은 평일로 되어 있으나, AutoGetServiceDay 함수를 통해 외부에서 정보를 받아옵니다.
'''
LineList = SettingsManager.GetLineTotal()
StationList = csvread.GetStationList()
HolidayOptionList = ["평일","토요일","휴일"]

LineSelection = SettingsManager.StationLoad()[SettingsManager.MagicWord_Line]
StationLoad = SettingsManager.StationLoad()[SettingsManager.MagicWord_Station]

'''
오류를 막기 위해 마지막으로 선택한 역이 해당 실제로 목록에 없을 경우 이를 무시하고 StationList의 7번째 인덱스 값으로 바꾸는 구문입니다.
'''
if StationLoad in StationList :
    StationSelection = StationLoad
else :
    StationSelection = StationList[7]
    
HolidaySelection = HolidayOptionList[0]

'''
Tkinter를 이용하여 메인 창을 만들기 위한 구문입니다. 마스터(루트)윈도우 클래스 명은 win으로 되어 있습니다.
'''
win = tk.Tk()
win.title(f'열차 시간 알리미')
win.geometry(f'-{default_x_po}-{default_y_po}')
#win.minsize(230,150)
win.resizable(False, False)
win.attributes("-topmost", 1)

##메인 창을 한 번 클릭시 도착 예정 시각 정보를 표시하기 위한 구문입니다.
win.bind("<Button-1>", lambda e: ToggleLabelVisibility())

'''
##메인 창 더블 클릭 시 시간표 창을 열기위한 구문입니다.
win.bind("<Double-Button-1>", lambda e: TimeTableWindow.TimeTableWindowOpen(MasterWindow = win,
                                                                            StationSelection = StationSelection,
                                                                            HolidaySelection=HolidaySelection ))
'''

##메인 창 종료시 설정을 저장하기위한 구문입니다.
win.protocol("WM_DELETE_WINDOW", lambda : [SettingsManager.StationSave(line = LineSelection, station=StationSelection), win.destroy()])

##메인 창 UI를 꾸미는 부분입니다.

###상단 메뉴바 설정
LineRadioOption=tk.IntVar()
LineRadioOption.set(LineSelection)
StationRadioOption=tk.StringVar()
StationRadioOption.set(StationSelection)
HolidayRadioOption=tk.StringVar()
HolidayRadioOption.set(HolidaySelection)


menubar = tk.Menu(master = win)

menu_settings = tk.Menu(menubar, tearoff=0)

menu_line = tk.Menu(menu_settings, tearoff=0)
for LineOption in LineList:
    menu_line.add_radiobutton(label=f'{LineOption} 호선', variable=LineRadioOption, value = LineOption, command = lambda: ChangeLine(LineRadioOption.get()))

menu_station = tk.Menu(menu_settings, tearoff=0)
for StationOption in StationList:
    menu_station.add_radiobutton(label=StationOption, variable=StationRadioOption, value = StationOption, command=lambda: ChangeStation(StationRadioOption.get()))

menu_holiday = tk.Menu(menubar, tearoff=0)
for HolidayOption in HolidayOptionList:
    menu_holiday.add_radiobutton(label=HolidayOption, variable=HolidayRadioOption, value = HolidayOption, command = lambda: ChangeHoliday(HolidayRadioOption.get()))


menubar.add_command(label="시간표 검색", command = lambda: TimeTableWindow.TimeTableWindowOpen(MasterWindow = win,
                                                                            StationSelection = StationSelection,
                                                                            HolidaySelection=HolidaySelection) )

menu_settings.add_cascade(label="호선 설정", menu = menu_line)
menu_settings.add_cascade(label="역 설정", menu = menu_station)
menu_settings.add_cascade(label="휴일 설정", menu = menu_holiday)
menubar.add_cascade(label="설정", menu = menu_settings)
menubar.add_command(label="?", command = lambda: HelpWindow.HelpOpen(MasterWindow=win, Line=int(LineSelection)))
win.config(menu=menubar)

###메인 프레임 구성
MFrame = tk.LabelFrame(master = win, labelanchor="n", text=f'{StationSelection} / {HolidaySelection}',cursor="hand2")
MFrame.pack(fill=tk.BOTH, expand=True)

###서브 프레임 구성
SFrameTOP = tk.LabelFrame(master = MFrame, labelanchor="n", text=f'{StationList[0]} 방면')
SFrameTOP.pack(fill=tk.BOTH, padx = 10, pady = 5, expand=True)

SFrameBOT = tk.LabelFrame(master = MFrame, labelanchor="n", text=f'{StationList[-1]} 방면')
SFrameBOT.pack(fill=tk.BOTH, padx = 10, pady = 5, expand=True)

###시간 프레임 구성
TFrameTOP0 = tk.LabelFrame(master = SFrameTOP, labelanchor="n", text="이번 열차")
TFrameTOP0.pack(fill=tk.BOTH, padx = 5, pady = 5, expand=True, side=tk.LEFT)
TFrameTOP1 = tk.LabelFrame(master = SFrameTOP, labelanchor="n",text="다음 열차")
TFrameTOP1.pack(fill=tk.BOTH, padx = 5, pady = 5, expand=True, side=tk.LEFT)

TFrameBOT0 = tk.LabelFrame(master = SFrameBOT, labelanchor="n", text="이번 열차")
TFrameBOT0.pack(fill=tk.BOTH, padx = 5, pady = 5, expand=True, side=tk.LEFT)
TFrameBOT1 = tk.LabelFrame(master = SFrameBOT, labelanchor="n",text="다음 열차")
TFrameBOT1.pack(fill=tk.BOTH, padx = 5, pady = 5, expand=True, side=tk.LEFT)

###라벨 구성
Tstr0 = tk.StringVar()
Tstr0.set("-")
Tstr1 = tk.StringVar()
Tstr1.set("-")
Tstr2 = tk.StringVar()
Tstr2.set("-")
Tstr3 = tk.StringVar()
Tstr3.set("-")

Tstr4 = tk.StringVar()
Tstr4.set("-")
Tstr5 = tk.StringVar()
Tstr5.set("-")
Tstr6 = tk.StringVar()
Tstr6.set("-")
Tstr7 = tk.StringVar()
Tstr7.set("-")

TLabelTOPU0 = tk.Label(master=TFrameTOP0, textvariable=Tstr0)
TLabelTOPU0.pack()
TLabelTOPD0 = tk.Label(master=TFrameTOP0, textvariable=Tstr1)
#TLabelTOPD0.pack()

TLabelTOPU1 = tk.Label(master=TFrameTOP1, textvariable=Tstr2)
TLabelTOPU1.pack()
TLabelTOPD1 = tk.Label(master=TFrameTOP1, textvariable=Tstr3)
#TLabelTOPD1.pack()

TLabelBOTU0 = tk.Label(master=TFrameBOT0, textvariable=Tstr4)
TLabelBOTU0.pack()
TLabelBOTD0 = tk.Label(master=TFrameBOT0, textvariable=Tstr5)
#TLabelBOTD0.pack()

TLabelBOTU1 = tk.Label(master=TFrameBOT1, textvariable=Tstr6)
TLabelBOTU1.pack()
TLabelBOTD1 = tk.Label(master=TFrameBOT1, textvariable=Tstr7)
#TLabelBOTD1.pack()

##UI 구성 끝


