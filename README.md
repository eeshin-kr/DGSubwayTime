# 열차 시간 알리미 (DGSubwayTime) 🚇 
대구 도시철도 열차의 도착 시간을 시간표 기반으로 알려주는 프로그램 (파이썬 tkinter로 제작)

## 프로그램 사진

메인 창

![메인 창 사진](https://user-images.githubusercontent.com/60684821/174765424-98a0ffcf-2ba3-44b0-83ee-74f0521a60a5.jpg)

시간표 창

![Annotation 2022-06-21 181858](https://user-images.githubusercontent.com/60684821/174765431-6ad8fdf2-3fb9-4aa2-9192-52258a31a5f1.jpg)
![Annotation 2022-06-21 181911](https://user-images.githubusercontent.com/60684821/174765435-0513943b-f2ba-411a-bdad-88ebacf487a8.jpg)


## 요구사항
* 파이썬 3.10+ (3.10.4에서 테스트 됨)
* Windows 10 (타 OS에서는 시험해보지 않음)

## 특징
* tkinter를 이용한 GUI 프로그램으로 구성하였습니다.
* 공식 시간표를 이용하여 도착시간을 계산합니다.
* 파이썬 표준 모듈만 사용, 모듈 설치 필요 없습니다.
* 평일/토요일/휴일 여부를 시작할 때, 정해진 시간에 네이버 지도로 부터 받아옵니다.
* 열차 시간표 데이터를 공공데이터 포털(data.go.kr)로 부터 자동으로 받아옵니다.
  * 프로그램 시작 시 시간표 파일에 변경 있을 경우 최신 버전 교체 알림 기능이 존재합니다.
  * 파일이 존재하지 않을 경우 알림창을 통해 다운로드 여부를 선택 가능합니다.
* 사용자의 마지막 호선/열차 선택 값을 Settings.ini에 저장, 불러오기 가능합니다.
* TreeView를 통한 열차별 도착 시간을 볼 수 있습니다.

## 주의사항
* 시간표 기준으로 동작하여 실제와 차이가 있을 수 있습니다.
* 해당 역의 도착 시간을 기준으로 합니다.
  * 단, 열차의 출발지는 도착시간이 아닌 출발시간을 기준으로 합니다.
  * 예) 1호선 설화명곡 -> 안심(종점) 기차의 경우 설화명곡 역에서 안심 방면 표시되는 시각은 열차의 출발 시각입니다.
  * 예) 2호선 문양 -> 영남대 기차의 경우 문양 역에서 영남대역 방면으로 표시되는 시각은 열차의 출발 시각입니다.

## 실행방법
Procesing, Scene 폴더 내의 모든 파일, Launch.pyw 파일을 받은 후 Launch.pyw를 실행합니다.

메인 창을 더블클릭하여 시간표를 열 수 있습니다.
