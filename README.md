<div align=center>

![header](https://capsule-render.vercel.app/api?type=Waving&color=gradient&height=300&section=header&text=Python%20Lottery%20Store&fontSize=70&animation=fadeIn&fontColor=FFFFFF)

  # LotteryStore_withPython
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=ffffff"/></a>
  
<div align=left>
 
### 개요
  사용자위치 주변의 복권판매점을 지도에 출력하고, 매 주차 복권당첨정보를 크롤링하여 표시하고 사용자의 복권당첨여부를 출력하며 복권번호를 추천하는 페이지를 제작할 예정입니다.
  
### 문제 정의와 과제의 필요성
  복권을 사려고 길을 헤매던 저의 경험을 토대로 다음과 같은 프로젝트를 계획하려 합니다. 네이버 지도, 카카오 지도에서는 복권판매점의 위치를 잘 나타내어주지 않습니다. 사용자 위치 주변의 복권판매점을 지도에서 확인하고, 복권의 당첨여부까지 확인할 수 있는 페이지가 있다면 보다 편리한 복권 구입이 될 것 같습니다. 
  
### 개발 개요
- Folium 모듈을 통해 지도를 시각화하고, 복권판매점주소 csv파일을 읽어와서 지도에 출력할 것입니다. <br>
- BeautifulSoup 모듈을 통해 네이버 복권당첨페이지에서 해당 정보를 크롤링하여 페이지에 출력하며 사용자의 입력된 복권번호와 이를 대조하여 당첨여부를 확인하는 기능을 구현할 것입니다. <br>
- 7개의 랜덤정수를 출력하는 함수를 제작하여 사용자에게 복권번호를 추천하는 기능을 구현할 예정입니다.
  
### 개발 계획
- [x] 5.21 – 프로젝트 계획서 작성 -> done
- [x] 5.23 ~ 5.25 – 복권판매점주소 csv 파일을 Folium map에 출력하는 기능 구현
- [ ] 5.26 ~ 5.28 – BeautifulSoup를 이용하여 웹 크롤링 후, 복권정보 출력 기능 구현
- [ ] 5.29 – 랜덤정수 7개 출력하는 함수 제작.
- [ ] 5.30 ~ 5.31 – 페이지 레이아웃 제작 및 코드 리팩토링 
  
### 계획 변경 내용
- 5.25 전국단위에서 서울시 노원구로 한정: pandas 데이터 추출과정 진행
  
  
  
![Footer](https://capsule-render.vercel.app/api?type=Waving&color=gradient&height=150&section=footer&animation=fadeIn) 
