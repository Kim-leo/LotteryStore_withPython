import json
import requests
from urllib.parse import urlparse
import pandas as pd
import folium
from bs4 import BeautifulSoup
import random

'''
csv파일의 모든 주소를 가져와서 이를 좌표로 변환하고
map에 핀을 찍어보도록 하겠습니다.

1. 카카오맵 API 가져오기
2. csv파일 가져오기
    2.1 도로명주소만 따로 뽑아서 저장하기
    2.2 도로명주소를 카카오API를 통해 좌표로 변환하기
    2.3 [위도, 경도]의 배열에서 각각 latitude, longitude 배열에 저장하기
3. 맵 생성하기
    3.1 맵 위에 좌표를 핀으로 모두 출력하기
4. 동행복권 사이트에서 당첨번호 7개와 몇회차인지 정보 크롤링하기
    4.1 당첨번호 7개를 배열에 저장
    4.2 N회차 + 날짜를 str으로 저장
    4.3 당첨확인 함수 생성
5. 랜덤번호 6개 생성 (1에서 45사이의 자연수)
'''

# 1. 카카오맵 API 가져오기
def getLatLon(addr):
    api_key = "c1291537d6477a23673e8a1b0f4702ff"
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": "KakaoAK {}".format(api_key)}
    result = json.loads(str(requests.get(url, headers=headers).text))
    match_first = result['documents'][0]['address']
    return [float(match_first['y']), float(match_first['x'])]

# 위의 함수 테스트 -> [위도, 경도] 배열로 출력 확인
getLatLon('서울 강북구 번동 469-25')

# 2. csv파일 가져오기
csv = pd.read_csv('/Users/kleo/Downloads/lottoAddress.csv', encoding = 'CP949')

nameAddr = csv[['상호', '도로명주소']]

# 2.1 위 데이터를 도로명주소만 따로 뽑아서 저장하기
# 배열 범위로 인해 서울 노원구로 축소
contains_Nowon = nameAddr['도로명주소'].str.contains('서울 노원구')
nowon = nameAddr[contains_Nowon]
addr = nowon['도로명주소'].sort_index()
addr = addr.reset_index(drop = True)

# 2.2 도로명주소를 카카오API를 통해 좌표로 변환하기
#2.3 [위도, 경도]의 배열에서 각각 latitude, longitude 배열에 저장하기
lat = []
lon = []
for i in addr:
    lat.append(getLatLon(i)[0])
    lon.append(getLatLon(i)[1])
    
# 3. 맵 생성하기
m = folium.Map(location = [lat[0], lon[0]], 
               zoom_start = 15, 
               width = 750, 
               height = 500)

# 3.1 맵 위에 좌표를 핀으로 모두 출력하기
for i in range(46):
    folium.Marker( [lat[i], lon[i]]).add_to(m)

    
    
# 4. 동행복권 사이트에서 당첨번호 7개와 몇회차인지 정보 크롤링하기
winBox = []
winBoxWithoutBonus = []
date = ''

def crawlURL():
    url = 'https://dhlottery.co.kr/common.do?method=main'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 4.1 당첨번호 7개를 배열에 저장
    global winBox
    global winBoxWithoutBonus
    global date
    for i in range(1, 7):
        winNums = soup.find('span', {'id': 'drwtNo{}'.format(i)})
        winBox.append(winNums.text)
    winBoxWithoutBonus = set(map(int, winBox))
    
    bonus = soup.find('span', {'id': 'bnusNo'})
    winBox.append(bonus.text)
    winBox = set(map(int, winBox)) #numBox를 int요소가 있는 set으로 저장. (추후 당첨확인을 위함.)

    # 4.2 N회차 + 날짜를 str으로 저장
    date = soup.find('a', {'id': 'goByWin1'})
    date = date.text
    
    print(winBox)
    print(date)
    print(winBoxWithoutBonus)
crawlURL()

# 4.3 당첨확인 함수 생성
def checkMyLuck():
    # 내 복권번호 6자리 입력하기
    N = 6
    myNumbers = []
    for i in range(N):
        myNumbers.append(int(input()))
    
    myNumbers.sort()
    myNumbers = set(myNumbers) #numBox와 본인의 번호를 비교를 위해 set으로 바꿈
    interNum = winBox & myNumbers
    howManyLucky = len(interNum) #등수를 확인하기 위해 얼마나 겹쳤는지 int로 확인
    
    # 1등 ~ 꽝 출력
    if len(winBox & myNumbers) == 6:
        if len(winBoxWithoutBonus & myNumbers) == 6:
            print("1등")
        else:
            print("2등")
    elif len(winBox & myNumbers) == 5:
        print("3등")
    elif len(winBox & myNumbers) == 4:
        print("4등")
    elif len(winBox & myNumbers) == 3:
        print("5등")
    else:
        print("꽝~")
    

checkMyLuck()    
    
# 5. 랜덤번호 6개 생성 (1에서 45사이의 자연수)
def randomNumbers():
    randomNumsList = random.sample(range(1,46), 6)
    randomNumsList.sort()
    
    print(randomNumsList)



