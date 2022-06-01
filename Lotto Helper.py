import json
import requests
from urllib.parse import urlparse
import pandas as pd
from bs4 import BeautifulSoup
import random
import tkinter as tk
import tkinter.font as tkFont
import tkintermapview


# 카카오맵 API 가져오기
def getLatLon(addr):
    api_key = "YOUR API KEY"
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": "KakaoAK {}".format(api_key)}
    result = json.loads(str(requests.get(url, headers=headers).text))
    match_first = result['documents'][0]['address']
    return [float(match_first['y']), float(match_first['x'])]

# 위의 함수 테스트 -> [위도, 경도] 배열로 출력 확인
getLatLon('서울 강북구 번동 469-25')

# csv파일 가져오기
csv = pd.read_csv('/Users/kleo/Downloads/lottoAddress.csv', encoding = 'CP949')

nameAddr = csv[['상호', '도로명주소']]

# 위 데이터를 도로명주소만 따로 뽑아서 저장하기
# 배열 범위로 인해 서울 노원구로 축소
contains_Nowon = nameAddr['도로명주소'].str.contains('서울 노원구')
nowon = nameAddr[contains_Nowon]
addr = nowon['도로명주소'].sort_index()
addr = addr.reset_index(drop = True)

# 도로명주소를 카카오API를 통해 좌표로 변환하기
# [위도, 경도]의 배열에서 각각 latitude, longitude 배열에 저장하기
lat = []
lon = []
for i in addr:
    lat.append(getLatLon(i)[0])
    lon.append(getLatLon(i)[1])
    
# 동행복권 사이트에서 당첨번호 7개와 몇회차인지 정보 크롤링하기
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
    winBoxWithoutBonus = sorted(winBoxWithoutBonus)
    
    bonus = soup.find('span', {'id': 'bnusNo'})
    winBox.append(bonus.text)
    winBox = set(map(int, winBox)) #numBox를 int요소가 있는 set으로 저장. (추후 당첨확인을 위함.)
    winBox = sorted(winBox)

    # 4.2 N회차 + 날짜를 str으로 저장
    date = soup.find('a', {'id': 'goByWin1'})
    date = date.text
    
    #print(winBox)
    #print(date)
    #print(winBoxWithoutBonus)
crawlURL()

import tkinter as tk
import tkinter.font as tkFont
import tkintermapview

window = tk.Tk()
window.title('for test page')
window.geometry('640x400+100+100')
window.resizable(False, False)
 

titleFont = tkFont.Font(family='Lucida Grande', size = 30)
titleLabel = tk.Label(window, text = "Lotto helper", 
                      fg = 'snow', bg = 'green', 
                      font = titleFont)
titleLabel.place(x = 230, y = 10)
 
# 지도 띄우기
map_widget = tkintermapview.TkinterMapView(window, width = 330, height = 250, corner_radius = 0)
map_widget.set_position(lat[0], lon[0])
map_widget.set_zoom(15)
for i in range(46):
    markers = map_widget.set_marker(lat[i], lon[i])

# 복권번호 확인 레이블
winBox = list(winBox)
winDateLabel = tk.Label(window, text = date, 
                        fg = 'snow', bg = 'green', 
                        width = 30, height = 2)

winBoxLabel1 = tk.Label(window, text = winBox[0], width = 2,
                       fg = 'snow', bg = 'green')
winBoxLabel2 = tk.Label(window, text = winBox[1], width = 2,
                        fg = 'snow', bg = 'green')
winBoxLabel3 = tk.Label(window, text = winBox[2], width = 2,
                        fg = 'snow', bg = 'green')
winBoxLabel4 = tk.Label(window, text = winBox[3], width = 2,
                        fg = 'snow', bg = 'green')
winBoxLabel5 = tk.Label(window, text = winBox[4], width = 2,
                        fg = 'snow', bg = 'green')
winBoxLabel6 = tk.Label(window, text = winBox[5], width = 2,
                        fg = 'snow', bg = 'green')
winBoxLabelPlus = tk.Label(window, text = "+", width = 2,
                        fg = 'snow', bg = 'green')
winBoxLabelBonus = tk.Label(window, text = winBox[6], width = 2,
                        fg = 'snow', bg = 'green')

# 당첨확인 레이블
textBox1 = tk.Entry(window, width = 30, textvariable=int)
resultLabel = tk.Label(window, text = "결과 표시 창", width  = 30,
                       fg = 'snow', bg = 'green')
infoLabel1 = tk.Label(window, text = "번호 입력 시, 다음과 같이 입력해주세요.", 
                     width = 30, height = 2, fg = 'snow', bg = 'green')
infoLabel2 = tk.Label(window, text = "1 2 3 4 5 6 7", 
                     width = 30, height = 2, fg = 'green', bg = 'snow')

myNumbers = []

# 당첨확인 함수
def checkNumbers():
    
    global myNumbers
    global inputNumbers
    global winBox
    
    myNumbers = []
    
    myNumbers.append(textBox1.get().split(" "))
    inputNumbers = myNumbers[0]
    
    inputNumbers.sort()
    
    inputNumbers = set(map(int, inputNumbers)) #numBox와 본인의 번호를 비교를 위해 set으로 바꿈
    winBox = set(winBox)
    
    interNum = winBox & inputNumbers
    howManyLucky = len(interNum) #등수를 확인하기 위해 얼마나 겹쳤는지 int로 확인
    
    # 1등 ~ 꽝 출력
    if len(winBox & inputNumbers) == 6:
        if len(winBoxWithoutBonus & inputNumbers) == 6:
            resultLabel.configure(text = "1등")
        else:
            resultLabel.configure(text = "2등")
    elif len(winBox & inputNumbers) == 5:
        resultLabel.configure(text = "3등")
    elif len(winBox & inputNumbers) == 4:
        resultLabel.configure(text = "4등")
    elif len(winBox & inputNumbers) == 3:
        resultLabel.configure(text = "5등")
    else:
        resultLabel.configure(text = "꽝~")

checkBtn = tk.Button(window, width = 5, text = '클릭', command = checkNumbers)

# 랜덤번호 생성
randomNumsList = []
randomLabel = tk.Label(window, width = 30, height = 2,
                       fg = 'snow', bg = 'green')   

def randomNumbers():
    global randomNumsList
    randomNumsList = []
    randomNumsList = random.sample(range(1,46), 6)
    randomNumsList.sort()
    randomNumsString = ', '.join([str(elem) for elem in randomNumsList])
    
    randomLabel['text'] = randomNumsList
    

# 각 버튼 동작 함수
def printMapBtn():
    winDateLabel.place_forget()
    winBoxLabel1.place_forget()
    winBoxLabel2.place_forget()
    winBoxLabel3.place_forget()
    winBoxLabel4.place_forget()
    winBoxLabel5.place_forget()
    winBoxLabel6.place_forget()
    winBoxLabelPlus.place_forget()
    winBoxLabelBonus.place_forget()
    randomLabel.place_forget()
    
    map_widget.place(x = 250, y = 100)

def showWinNumsBtn():
    map_widget.place_forget()
    infoLabel1.place_forget()
    infoLabel2.place_forget()
    textBox1.place_forget()
    checkBtn.place_forget()
    resultLabel.place_forget()
    randomLabel.place_forget()
    
    winDateLabel.place(x = 250, y = 100)
    winBoxLabel1.place(x = 250, y = 170)
    winBoxLabel2.place(x = 280, y = 170)
    winBoxLabel3.place(x = 310, y = 170)
    winBoxLabel4.place(x = 340, y = 170)
    winBoxLabel5.place(x = 370, y = 170)
    winBoxLabel6.place(x = 400, y = 170)
    winBoxLabelPlus.place(x = 450, y = 170)
    winBoxLabelBonus.place(x = 500, y = 170)
    
def checkMyNumbersBtn():
    map_widget.place_forget()
    winDateLabel.place_forget()
    winBoxLabel1.place_forget()
    winBoxLabel2.place_forget()
    winBoxLabel3.place_forget()
    winBoxLabel4.place_forget()
    winBoxLabel5.place_forget()
    winBoxLabel6.place_forget()
    winBoxLabelPlus.place_forget()
    winBoxLabelBonus.place_forget()
    randomLabel.place_forget()
    
    infoLabel1.place(x = 250, y = 100)
    infoLabel2.place(x = 250, y = 140)
    textBox1.place(x = 250, y = 200)
    checkBtn.place(x = 350, y = 250)
    resultLabel.place(x = 250, y = 300)
    return
 
def randomNumberBtn():
    map_widget.place_forget()
    winDateLabel.place_forget()
    winBoxLabel1.place_forget()
    winBoxLabel2.place_forget()
    winBoxLabel3.place_forget()
    winBoxLabel4.place_forget()
    winBoxLabel5.place_forget()
    winBoxLabel6.place_forget()
    winBoxLabelPlus.place_forget()
    winBoxLabelBonus.place_forget()
    infoLabel1.place_forget()
    infoLabel2.place_forget()
    textBox1.place_forget()
    checkBtn.place_forget()
    resultLabel.place_forget()
    
    randomNumbers()
    randomLabel.place(x = 250, y = 200)

# 각 버튼 생성
btn1 = tk.Button(window, text = '노원구 복권판매점', width = 10, height = 2, command = printMapBtn)
btn1.place(x = 50, y = 100)
 
btn2 = tk.Button(window, text = '복권번호 확인', width = 10, height = 2, command = showWinNumsBtn)
btn2.place(x = 50, y = 170)
 
btn3 = tk.Button(window, text = '당첨 조회', width = 10, height = 2, command = checkMyNumbersBtn)
btn3.place(x = 50, y = 240)

btn4 = tk.Button(window, text = '복권번호 추천', width = 10, height = 2, command = randomNumberBtn)
btn4.place(x = 50, y = 310)

window.mainloop()


