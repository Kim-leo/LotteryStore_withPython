import json
import requests
from urllib.parse import urlparse
import pandas as pd
import folium

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
