'''
시간표 창을 표시하기 위한 모듈입니다.
'''
import tkinter as tk
from tkinter import ttk
from Processing import csvread

def TimeTableWindowOpen(event = None, MasterWindow = None, StationSelection="용산", HolidaySelection="평일"):
    '''
    시간표 창을 표시하기 위한 함수입니다.
    시간표 창은 역사별 / 열차별 시간표가 Notebook을 이용해 탭으로 구분되어 있습니다.
    역사별 시간표 창은 리스트 박스를 통해현재 역사의 시간표를 나열하며, 열차별 시간표 창은 트리뷰를 통해 하루동안의 열차 전체를 조회합니다.
    '''
    StationList = csvread.GetStationList()
    HolidayOptionList = ["평일","토요일","휴일"]

    TableWin = tk.Toplevel(MasterWindow)
    TableWin.title(f'시간표')
    #TableWin.grab_set() #시간창 표시 시 메인 창을 제어하지 못하게 설정
    '''
    시간표 창의 위치를 정하는 부분입니다. 메인 창의 위치에 따라 표시 위치가 달라집니다.
    '''
    
    if MasterWindow.winfo_x()< 500 :
        TableWin.geometry(f'350x400+{MasterWindow.winfo_x()+200}+{MasterWindow.winfo_y()-300}')
    else:
        TableWin.geometry(f'350x400+{MasterWindow.winfo_x()-400}+{MasterWindow.winfo_y()-300}')

    #메인 UI 구성
    NoteBook = ttk.Notebook(TableWin)
    NoteBook.pack(fill=tk.BOTH, expand=True, pady = 2)
    
    Frame1 = tk.Frame(master = NoteBook)
    Frame1.pack(fill=tk.BOTH, expand=True)
    Frame2 = tk.Frame(master = NoteBook)
    Frame2.pack(fill=tk.BOTH, expand=True)
    NoteBook.add(Frame1, text="역사별 시간표")
    NoteBook.add(Frame2, text="열차별 시간표")
    
    ##역사별 시간표 UI 구성
    TFrame1 = tk.LabelFrame(master = Frame1, labelanchor="n", text="역 설정") # expand=True 시에 화면 크기 조정 시 UI가 뭉개짐
    TFrame1.pack(fill=tk.X, expand=False)
    TFrame2 = tk.LabelFrame(master = Frame1, labelanchor="n", text="휴일 설정")
    TFrame2.pack(fill=tk.X, expand=False)
    TFrame3 = tk.LabelFrame(master = Frame1, labelanchor="n", text=f'{StationList[0]}방면')
    TFrame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    TFrame4 = tk.LabelFrame(master = Frame1, labelanchor="n", text=f'{StationList[-1]}방면')
    TFrame4.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)   
    TStationSelect = tk.StringVar()
    TStationSelect.set(StationSelection)  
    TComboBox = ttk.Combobox(master = TFrame1, textvariable = TStationSelect)
    TComboBox['values'] = StationList
    TComboBox.pack(fill=tk.X, expand=True, padx= 2, pady = 2)
    TComboBox.bind('<<ComboboxSelected>>', lambda e: UpdateTimeTableTopWindow(THolidaySelect.get(),
                                                                              TStationSelect.get(),
                                                                              TListBoxLEFT,
                                                                              TListBoxRIGHT,
                                                                              StationSelection,
                                                                              HolidaySelection))
    TComboBox.bind('<Return>', lambda e: UpdateTimeTableTopWindow(THolidaySelect.get(),
                                                                  TStationSelect.get(),
                                                                  TListBoxLEFT,
                                                                  TListBoxRIGHT,
                                                                  StationSelection,
                                                                  HolidaySelection))
    THolidaySelect = tk.StringVar()
    THolidaySelect.set(HolidaySelection)
    for txt in HolidayOptionList:           
        TRadioButton = tk.Radiobutton(master=TFrame2, text=txt, variable=THolidaySelect, value=txt, command= lambda : UpdateTimeTableTopWindow(THolidaySelect.get(),
                                                                                                                                               TStationSelect.get(),
                                                                                                                                               TListBoxLEFT,
                                                                                                                                               TListBoxRIGHT,
                                                                                                                                               StationSelection,
                                                                                                                                               HolidaySelection))
        TRadioButton.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
    TScrollBarLEFT = tk.Scrollbar(master = TFrame3)
    TScrollBarRIGHT = tk.Scrollbar(master = TFrame4)
    
    TListBoxLEFT = tk.Listbox(master=TFrame3, selectmode="browse",selectbackground="orange", yscrollcommand = TScrollBarLEFT.set)
    TListBoxLEFT.pack(fill=tk.BOTH, side=tk.LEFT, padx = 2, pady=5 ,expand=True)

    TListBoxRIGHT = tk.Listbox(master=TFrame4, selectmode="browse", selectbackground="orange", yscrollcommand=TScrollBarRIGHT.set)
    TListBoxRIGHT.pack(fill=tk.BOTH, side=tk.LEFT, padx = 2, pady=5 ,expand=True)
    
    TScrollBarLEFT.pack(fill = tk.Y, side= tk.LEFT, padx=2, pady=5, expand=False)
    TScrollBarLEFT.config(command = TListBoxLEFT.yview)
    TScrollBarRIGHT.pack(fill = tk.Y, side= tk.LEFT, padx=2, pady=5, expand=False)
    TScrollBarRIGHT.config(command = TListBoxRIGHT.yview)

    
    ## 리스트 박스에 시간표 채워넣는 기능
    UpdateTimeTableTopWindow(THolidaySelect.get(),TStationSelect.get(),TListBoxLEFT,TListBoxRIGHT, StationSelection, HolidaySelection)
    
    ##열차 번호별 시간표 UI 구성
    Frame2.columnconfigure(1, weight=1)
    Frame2.rowconfigure(0, weight=1)

    ScrollX = tk.Scrollbar(master = Frame2, orient = tk.HORIZONTAL)
    ScrollY = tk.Scrollbar(master = Frame2, orient = tk.VERTICAL)

    TreeView = ttk.Treeview(master = Frame2)
    TreeView.config(selectmode = 'extended', xscrollcommand = ScrollX.set, yscrollcommand = ScrollY.set)
    TreeView.grid(row=0, column=1, sticky="nswe")

    ScrollX.grid(row = 1, column = 1, sticky = "ew")
    ScrollX.config(command=TreeView.xview)
    ScrollY.grid(row = 0, column = 2, sticky = "sn")
    ScrollY.config(command = TreeView.yview)

    TVOptionframe = tk.Frame(master = Frame2)
    TVOptionframe.grid(row=0, column=0, sticky="sn")
    TFrame2_1 = tk.LabelFrame(master = TVOptionframe, text="방면", labelanchor="n")
    TFrame2_1.pack(fill = tk.BOTH)
    TFrame2_2 = tk.LabelFrame(master = TVOptionframe, text="휴일", labelanchor="n")
    TFrame2_2.pack(fill = tk.BOTH)
    UDv = tk.StringVar(TFrame2_1, "상")
    FirstDep = [csvread.GetStationList()[0], "상"]
    LastDep = [csvread.GetStationList()[-1], "하"]
    DepList = [FirstDep, LastDep]
   
    for (Sta, Dep) in DepList:
        RButton1 = tk.Radiobutton(master = TFrame2_1, text = f'{Sta} 방면', variable = UDv, value = Dep, command = lambda: ModifyTreeview(TreeView,
                                                                                                                                        UDv.get(),
                                                                                                                                        HDv.get(),
                                                                                                                                        TStationSelect.get(),
                                                                                                                                        StationSelection,
                                                                                                                                        HolidaySelection) )
        RButton1.pack(side=tk.TOP, anchor="w")

    HDv = tk.StringVar(TFrame2_2, HolidaySelection)
    
    Holidays = HolidayOptionList

    for (txt) in Holidays:
        RButton2 = tk.Radiobutton(master = TFrame2_2, text=txt, variable=HDv, value=txt, command = lambda: ModifyTreeview(TreeView,
                                                                                                                          UDv.get(),
                                                                                                                          HDv.get(),
                                                                                                                          TStationSelect.get(),
                                                                                                                          StationSelection,
                                                                                                                          HolidaySelection ) )
        RButton2.pack(side=tk.TOP, anchor="w")

    SizeGrip = ttk.Sizegrip(master = Frame2)
    SizeGrip.grid(row=1, column=2, sticky=tk.SE)

    UpdateNoteBookSize(Toplevel = TableWin, Notebook = NoteBook)
    ModifyTreeview(TreeView, UDv.get(), HDv.get(), TStationSelect.get(), StationSelection, HolidaySelection )
    ##UI 꾸미는 부분 끝

    NoteBook.bind("<<NotebookTabChanged>>",lambda e: UpdateNoteBookSize(Toplevel = TableWin, Notebook = NoteBook))
    
    TableWin.mainloop() ##mainloop가 실행되지 않으면 위젯의 초기값이 설정되지 않는다.

    
def UpdateTimeTableTopWindow(THolidaySelection = None,
                             TStationSelection = None,
                             TListBoxLEFT=None,
                             TListBoxRIGHT=None,
                             StationSelection = None,
                             HolidaySelection = None):
    '''
    역사별 시간표의 리스트박스를 새로고침하기 위한 함수입니다.
    '''
    
    TListBoxLEFT.delete(0, TListBoxLEFT.size()) #리스트 박스 초기화
    TListBoxRIGHT.delete(0, TListBoxRIGHT.size())

    TimeTableContentLEFT = csvread.GetTimeTable(week = THolidaySelection, direction = "상", station = TStationSelection)
    #TimeTableContentNEWLEFT = zip(list(range(len(TimeTableContentLEFT))), TimeTableContentLEFT) #리스트에 넣기 쉽게 [인덱스 번호, 내용]으로 변환
    
    TimeTableContentRIGHT = csvread.GetTimeTable(week = THolidaySelection, direction = "하", station = TStationSelection)
    #TimeTableContentNEWRIGHT = zip(list(range(len(TimeTableContentLEFT))), TimeTableContentRIGHT)

    NowTrainUP = csvread.TimeTableSearch(direction="상", station=StationSelection, week=HolidaySelection)[0] #이번 열차 받아오기 위함
    NowTrainDOWN = csvread.TimeTableSearch(direction="하", station=StationSelection, week=HolidaySelection)[0]
    
    ScrollPatch = [0,0] #이번 열차까지 스크롤 위치를 저장하기 위함
    TempHour = ["",""] #리스트 박스 내 시간대 별로 나누기 위함
    for TimeTableContent in TimeTableContentLEFT:
        
        if TempHour[0] != TimeTableContent[:2] :
            TListBoxLEFT.insert(TListBoxLEFT.size(), f'*****{TimeTableContent[:2]}시*****')
            TempHour[0] = TimeTableContent[:2]
           

        if (THolidaySelection == HolidaySelection and
            TStationSelection == StationSelection and
            TimeTableContent == NowTrainUP):
          
            TListBoxLEFT.insert(TListBoxLEFT.size(), TimeTableContent[:-3] + " (이번 열차)") #초는 제외하고 표시
            ScrollPatch[0] = TListBoxLEFT.size()-1
            
        else:
            TListBoxLEFT.insert(TListBoxLEFT.size(), TimeTableContent[:-3])

            
    for TimeTableContent in TimeTableContentRIGHT:
        if TempHour[1] != TimeTableContent[:2] :
            TListBoxRIGHT.insert(TListBoxRIGHT.size(), f'*****{TimeTableContent[:2]}시*****')
            TempHour[1] = TimeTableContent[:2]
            
        if (THolidaySelection == HolidaySelection and
            TStationSelection == StationSelection and
            TimeTableContent == NowTrainDOWN):
          
            TListBoxRIGHT.insert(TListBoxRIGHT.size(), TimeTableContent[:-3] + " (이번 열차)") #초는 제외하고 표시
            ScrollPatch[1] = TListBoxRIGHT.size()-1
            
        else:
            TListBoxRIGHT.insert(TListBoxRIGHT.size(), TimeTableContent[:-3])

    if len(TimeTableContentLEFT) == 0: ##시간표를 제대로 불러오지 못했을 경우
        TListBoxLEFT.insert(0, "역 명을 확인하십시오")

    #편리함을 위해 리스트박스에서 이번 열차 선택
    TListBoxLEFT.see(ScrollPatch[0])
    TListBoxRIGHT.see(ScrollPatch[1])
    TListBoxLEFT.selection_set(ScrollPatch[0])
    TListBoxRIGHT.selection_set(ScrollPatch[1])
    

def ModifyTreeview(tv, UPval="상", HDval="평일", TStationSelection = "용산",
                   StationSelection = "용산",HolidaySelection = "평일"):
    '''
    열차별 시간표 창의 트리뷰 내용을 새로고침하는 함수입니다.
    '''
    for i in tv.get_children(): ##Treeview 내용 제거
        tv.delete(i)
 
    if UPval == "상":
        tv['columns'] = ['열차번호'] + csvread.GetStationList()[::-1]
    else :
        tv['columns'] = ['열차번호'] + csvread.GetStationList()

    tv['show'] = 'headings'

    for col in tv['columns']:
        tv.column(col, anchor=tk.CENTER, width=100, stretch=False) 
        tv.heading( col, text=col, anchor=tk.CENTER)
        
    NowTrainUP = csvread.TimeTableSearch(direction="상", station=StationSelection, week=HolidaySelection)[0] #이번 열차 받아오기 위함
    NowTrainDOWN = csvread.TimeTableSearch(direction="하", station=StationSelection, week=HolidaySelection)[0]
    CurrentStationIndex = csvread.GetStationList().index(StationSelection)
    
    TrainDict = csvread.GetTimeTable2(week=HDval, direction = UPval)
    
    for key, val in TrainDict.items():
        newlist = [key]
        if UPval == "상" :
            newlist.extend(val[::-1])
        else:
            newlist.extend(val)
        tv.insert(parent='', index='end', iid=key, values=newlist)
        
        if (HDval == HolidaySelection and
            TStationSelection == StationSelection):
            if UPval == "상" and val[CurrentStationIndex] == NowTrainUP:
                tv.see(key)
                tv.selection_set(key)
                newlist[0] = newlist[0] + "(이번 열차)"
                tv.item(key, values = newlist)

            elif UPval == "하" and val[CurrentStationIndex] == NowTrainDOWN:
                tv.see(key)
                tv.selection_set(key)
                newlist[0] = newlist[0] + "(이번 열차)"
                tv.item(key, values = newlist)
                
                


def UpdateNoteBookSize(Toplevel = None, Notebook=None, event=None):
    '''
    시간표 창의 크기를 설정하는 함수입니다.
    사용의 편의성을 위해 탭 선택에 따라서 다른 크기를 설정합니다.
    '''
    #DefaultSize = {0: "350x350", 1: "500x350"}
    DefaultMinSize = {0: [350, 350], 1: [500, 350]}
    DefaultMaxSize = {0: [350, False], 1: [False, False]}
    DefaultReSizAble = {0: [False, True], 1: [True, True]}
    CurrentIndex = Notebook.index(Notebook.select())

    Toplevel.minsize(DefaultMinSize[CurrentIndex][0], DefaultMinSize[CurrentIndex][1])
    Toplevel.maxsize(DefaultMaxSize[CurrentIndex][0], DefaultMaxSize[CurrentIndex][1])
    Toplevel.resizable(DefaultReSizAble[CurrentIndex][0], DefaultReSizAble[CurrentIndex][1])


