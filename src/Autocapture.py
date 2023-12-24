# import pyautogui
# # snapshot = ImageGrab.grab()
# Pos = [0,1,2,3]
# number = 0
# region = (100, 100, 200, 200)
# while True:
#     # for i in range(2):
#     #     input("press enter")
#     #     Pos[i] = pyautogui.position()
#     #     i +=1
#     # img = pyautogui.screenshot(region=(Pos[0] ,Pos[1], Pos[2], Pos[3]))
#     pyautogui.moveTo(150, 150, duration=1, region=region)
#     pyautogui.click(button='left', region=region)
#     number = number + 1
#     path = "D:\\Project\\AutoCapture\\my_screenshot1" + str(number) +".png"
#     img.save(path)

import tkinter as tk
import pyautogui
import keyboard
from PIL import ImageTk, Image
import mss

# Khởi tạo cửa sổ tkinter
window = tk.Tk()

# Đặt cửa sổ thành full screen
window.geometry("400x300")

# window.attributes('-alpha', 0.5)

# # Xác định và hiển thị kích thước màn hình
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
canvas = tk.Canvas(window, width=screen_width, height=screen_height)
canvas.pack()

# Thiết lập các biến để lưu vùng (region)
top_left = None
bottom_right = None
is_selecting = False

def on_keyboard_press(event):
    global top_left, is_selecting
    global bottom_right
    if event.name == 'r' and is_selecting == False:  # Nhấn phím 'r' để bắt đầu chọn vùng
        is_selecting = True
        print("r press")
        top_left = (window.winfo_pointerx(), window.winfo_pointery())
    if event.name == 'x' and is_selecting:
         print("r dont't press")
         bottom_right = (window.winfo_pointerx(), window.winfo_pointery())
         is_selecting = False
        #  window.destroy()
    if event.name == 'f3':
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # gia tri 1 OR 0
            print(sct.monitors[1])
            print(sct.monitors[0])
            
            region = {
            "left": monitor["left"] + min(top_left[0], bottom_right[0]),
            "top": monitor["top"] + min(top_left[1], bottom_right[1]),
            "width": abs(top_left[0] - bottom_right[0]),
            "height": abs(top_left[1] - bottom_right[1])
            }
            print(region)
            screenshot = sct.grab(region)
            path = "D:\\Project\\AutoCapture\\my_screenshot1" + '1' +".png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
    
                
# Gắn các hàm xử lý sự kiện vào bàn phím
keyboard.on_press(on_keyboard_press)
# keyboard.on_release(on_keyboard_release)

# Chạy vòng lặp chính của tkinter
window.mainloop()