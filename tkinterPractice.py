import tkinter as tk
import tkinter.font as tkFont
import tkintermapview

window = tk.Tk()
window.title('for test page')
window.geometry('640x400+100+100')
window.resizable(False, False)
 

titleFont = tkFont.Font(family='Lucida Grande', size = 30)

titleLabel = tk.Label(window, text = "Title label", 
                      fg = 'snow', bg = 'green', 
                      font = titleFont)
titleLabel.place(x = 230, y = 10)

 
map_widget = tkintermapview.TkinterMapView(window, width = 330, height = 250, corner_radius = 0)
map_widget.set_position(48.860381, 2.338594)
map_widget.set_zoom(15)

def printMap():
    map_widget.place(x = 250, y = 100)

def btn2Action():
    map_widget.place_forget()

 

btn1 = tk.Button(window, text = '버튼1의 텍스트', width = 20, height = 2, command = printMap)
btn1.place(x = 50, y = 100)
 
btn2 = tk.Button(window, text = '버튼2의 텍스트입니다.', width = 20, height = 2, command = btn2Action)
btn2.place(x = 50, y = 170)
 
btn3 = tk.Button(window, text = '버튼3', width = 20, height = 2)
btn3.place(x = 50, y = 240)

btn4 = tk.Button(window, text = '마지막 버튼', width = 20, height = 2)
btn4.place(x = 50, y = 310)

window.mainloop() 

 