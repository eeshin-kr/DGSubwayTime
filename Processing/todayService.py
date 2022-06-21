'''
외부에서 오늘이 평일/토요일/휴일인지 받아오기 위한 함수입니다.
'''
import time
import urllib.request
import urllib.error
import json

def GetTodayServiceDayNaver():
    '''
    모바일 네이버 지도에서 휴일 정보를 받아오는 함수입니다.
    '''
    try:
        CurrentTimeStr = time.strftime("%Y%m%d%H%M%S")
        NaverMapAPI = f'https://m.map.naver.com/pubtrans/getSubwayTimestamp.naver?inquiryDateTime={CurrentTimeStr}'
        DataURL = urllib.request.urlopen(NaverMapAPI)
        Data = DataURL.read()
        Encoding = DataURL.info().get_content_charset()
        jsonData = json.loads(Data.decode(Encoding))
        todayServiceDay = jsonData['result']['dateType']
        typeDict = {1: "평일",
                    2: "토요일",
                    3: "휴일"}
            
        return typeDict.get(todayServiceDay, "네이버에서 정확한 값을 받을 수 없습니다.")
        
    except urllib.error.HTTPError as e:
        print(e.__dict__)
        return "모듈로 부터 에러"
    


def GetTodayServiceDayNaverPC():
    '''
    PC 네이버 지도에서 휴일 정보를 받아오는 함수입니다. 파일 용량이 모바일 네이버 지도에서 받는 정보 보다 큽니다.
    '''
    try:
        NaverMapAPI = "https://map.naver.com/v5/api/transit/subway/stations/40230/schedule?lang=ko&stationID=40230"
        DataURL = urllib.request.urlopen(NaverMapAPI)
        Data = DataURL.read()
        Encoding = DataURL.info().get_content_charset()
        jsonData = json.loads(Data.decode(Encoding))
        todayServiceDay = jsonData['todayServiceDay']['name']

        return todayServiceDay
        
    except urllib.error.HTTPError as e:
        print(e.__dict__)
        return "모듈로 부터 에러"
