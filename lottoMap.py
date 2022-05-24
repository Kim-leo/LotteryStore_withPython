import json
import requests
from urllib.parse import urlparse
import pandas as pd
import folium

# 카카오맵 API를 이용하여 주소를 위도 경도로 출력하는 함수
# 주소입력 -> [위도, 경도] 배열형태로 출력
def getLatLng(addr):
    api_key = "Your API KEY"
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": "KakaoAK {}".format(api_key)}
    result = json.loads(str(requests.get(url, headers=headers).text))
    match_first = result['documents'][0]['address']
    return [float(match_first['y']), float(match_first['x'])]

#print(getLatLng("제주도 서귀포시 신서로 98번길 45 201호")[1]) -> 경도만 나옴

# 복권판매점 csv파일을 읽어오기
csv = pd.read_csv('/Users/kleo/Downloads/lottoAddress.csv', encoding = 'CP949')
address = csv["도로명주소"]
    
# 판매점 주소를 위도, 경도로 변환하기
latitude = []
longitude = []      

for i in range(10):
    latitude.append(getLatLng(address[i])[0])
    longitude.append(getLatLng(address[i])[1]) 
    
# 데이터프레임 만들기
df = pd.DataFrame({'이름': '상호', 
                           '상세주소': '도로명주소',
                           '주소': '주소',
                           '위도': latitude,
                           '경도': longitude})

# map 띄우기
lat = df['위도'][0]
lon = df['경도'][0]

m = folium.Map(location = [lat, lon],
               zoom_start = 17,
               width = 750,
               height = 500)
   
# latitude, longitude -> 맵에 핀 찍기
for i in range(10):
    folium.Marker( [latitude[i], longitude[i]]).add_to(m)


    

