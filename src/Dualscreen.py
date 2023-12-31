from tkinter import Tk, Button
import mss
from screeninfo import get_monitors

def capture_screen(screen_index):
    with mss.mss() as sct:
        monitors = get_monitors()
        if screen_index < len(monitors):
            monitor = monitors[screen_index]
            print("monitors" + format(screen_index) + ": " + format(monitor))
            print("monitor.x: "+ format(monitor.x))
            print("monitor.y: "+ format(monitor.y))
            region = {
                "left": monitor.x,
                "top": monitor.y,
                "width": monitor.width,
                "height": monitor.height,
            }
            screenshot = sct.grab(region)
            path = "D:\\Project\\AutoCapture\\img\\my_screenshot" + format(1) +".png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
            print(f"Đã chụp màn hình {screen_index} thành công.")

# Tạo cửa sổ giao diện
root = Tk()
root.title("Ứng dụng chụp màn hình")

# Tạo nút chụp màn hình màn số 1
capture_button1 = Button(root, text="Chụp màn hình 1", command=lambda: capture_screen(0))
capture_button1.pack()

# Tạo nút chụp màn hình màn số 2
capture_button2 = Button(root, text="Chụp màn hình 2", command=lambda: capture_screen(1))
capture_button2.pack()

root.mainloop()