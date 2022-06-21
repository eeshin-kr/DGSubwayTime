import tkinter as tk
from Processing import todayService
from Processing import DownloadSchedule
from Processing import SettingsManager
'''
메인 창의 ? 버튼 메뉴를 눌렸을 때 도움말 창을 표시하는 모듈입니다.
'''


'''
프로그램의 버전을 나타내기 위한 변수입니다.
별도의 모듈에서 해당 모듈로 버전명을 기록합니다.
'''
__version__ = ""
def HelpOpen(event = None, MasterWindow = None, Line = None):
    '''
    도움말 페이지를 구성하기위한 함수입니다.
    기본적인 정보와 시간표 최신화 여부 및 휴일 정보를 표시합니다.
    '''
    top = tk.Toplevel(MasterWindow)
    top.title(f'정보')
    top.transient(MasterWindow)
    if MasterWindow.winfo_x()< 500 :
        top.geometry(f'+{MasterWindow.winfo_x()+100}+{MasterWindow.winfo_y()}')
    else:
        top.geometry(f'+{MasterWindow.winfo_x()-300}+{MasterWindow.winfo_y()}')
    #top.attributes("-topmost", 1)
    top.resizable(False, False)
    #top.focus_force() ##강제로 포커스 이동시킴

    HFrame = tk.Frame(master=top)
    HFrame.pack()
    Label1 = tk.Label(master=HFrame, text=f'열차 시간 알리미 v{__version__}')
    Label1.pack()
    Label2 = tk.Label(master=HFrame, text="만든이: realoven@gmail.com")
    Label2.pack()
    Label3 = tk.Label(master=HFrame, text= f'''시간표 기반 열차 도착정보를 알려주는 프로그램,
프로그램이 실행될 때와 {SettingsManager.NextLaunchHour}시에 네이버 지도에서 오늘이 휴일인지 찾아옵니다.''')
    Label3.pack()
    Label4 = tk.Label(master=HFrame, text=f'현재 네이버 값: {todayService.GetTodayServiceDayNaver()}')
    Label4.pack()

    if DownloadSchedule.isUpdateAvailable(Line) ==  -1:
        UpdateVal = f'인터넷으로 부터 최신 정보를 받아올 수 없습니다.'
    elif DownloadSchedule.isUpdateAvailable(Line) :
        UpdateVal = f'재시작을 통해 현재 {Line}호선 시간표 업데이트가 필요합니다.'     
    else :
        UpdateVal = f'현재 {Line}호선 시간표가 최신버전입니다.'
    
        
    Label5 = tk.Label(master=HFrame, text=UpdateVal)
    Label5.pack()    
    Label6 = tk.Label(master=HFrame, text="시간표 출처(우클릭으로 열기): https://www.data.go.kr/data/3033376/fileData.do", fg="blue", cursor="hand2")
    Label6.pack()
    Label6.bind("<Button-3>", lambda e: webbrowser.open_new("https://www.data.go.kr/data/3033376/fileData.do"))
    top.bind("<Button-1>",lambda e: top.destroy())

    top.mainloop()

