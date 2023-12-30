from tkinter import Tk, ttk
from tkinter import *
# from Autocapture import *
import keyboard
import mss
from win32api import GetMonitorInfo, MonitorFromPoint    
    
font_text = ("normal",14)
list_mode = ["Mode1", "Mode2"]
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")

class Screen1:
    def __init__(self, root):
        self.root = root
        self.data = None
        self.start_x = 0
        self.start_y = 0
        self.stop_x = 1
        self.stop_y = 1
        
        self.count = 0
        status1 = "         "
        status2 = "                   "
        status1 = format(work_area[2]) + "x" + format(work_area[3])
        self.lbn_Mode1 = ttk.Label(root, text="Mode1:" + status1, borderwidth=1, relief="solid", font=font_text)
        self.lbn_Mode1.place(x = 0, y = 5)
        self.lbn_Mode2 = ttk.Label(root, text="Mode2:" + status2, borderwidth=1, relief="solid", font=font_text)
        # height = self.lbn_Mode1.winfo_reqheight() # # 26 pixel
        # print("Height:", height, "pixels")
        self.lbn_Mode2.place(x = 0, y = 35)
        self.bt_goto_screen2 = Button(root, text="Go to Screen 2", font=font_text, command=self.gotoScreen2)
        self.bt_goto_screen2.place(x = 0, y = 65)
        self.bt_show_data = Button(root,text = "Show data", font= font_text, command= self.showdata)
        self.bt_show_data.place(x = 0, y = 121)
        # height = self.bt_show_data.winfo_reqheight() # # 31 pixel
        # print("Height:", height, "pixels") 
        keyboard.on_press(self.on_key_press)
        
    def on_key_press(self,event):
        if event.name == "f2":
            pos = [self.start_x,self.start_y,self.stop_x,self.stop_y]
            self.captureRegion(pos)
        if event.name == "f3":
            pos = [0,0,work_area[2],work_area[3]]
            self.captureRegion(pos)  
        print("Key is pressed")
        
    def captureRegion(self,Pos):
        with mss.mss() as sct:
            monitors = sct.monitors
            monitor = sct.monitors[2]  # gia tri 1 OR 0        
            region = {
            "left": monitor["left"] + min(Pos[0], Pos[2]),
            "top": monitor["top"] + min(Pos[1], Pos[3]),
            "width": abs(Pos[0] - Pos[2]),
            "height": abs(Pos[1] - Pos[3])
            }
            print(region)
            screenshot = sct.grab(region)
            path = "D:\\Project\\AutoCapture\\img\\my_screenshot" + format(self.count) +".png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=path)
            print("Capture Region" + format(self.count))
            self.count += 1
                   
    def gotoScreen2(self):
        self.root.withdraw()  
        screen2 = Toplevel(self.root)
        screen2.attributes('-fullscreen',True)
        screen2.attributes('-alpha',0.1)
        self.data = [0,0,0,0]
        sc = Screen2(screen2)
        sc.set_value(self.data)
        
    def showdata(self):
        print("Show data")
        print(self.data)  
                
    def set_value(self,data):
        print("Set value: " + format(data))
        self.data =  data
        self.update_screen()
        
    def update_screen(self):
        self.start_x = self.data[0]
        self.start_y = self.data[1]
        self.stop_x = self.data[2]
        self.stop_y = self.data[3] 
        status2 = format(self.data[2] - self.data[0]) + "x" + format(self.data[3] - self.data[1])
        self.lbn_Mode2.config(text="Mode2:" + status2)


class Screen2:
    def __init__(self, root):
        self.root = root
        self.data = None
        self.canvas = Canvas(root, width=1920, height=1080)
        self.canvas.pack()
        global current_rectangle
        self.current_rectangle = None
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.stop_x = None
        self.stop_y = None
        self.canvas.bind("<Button-1>", self.start_capture)
        self.canvas.bind("<B1-Motion>", self.curent_capture)
        self.canvas.bind("<ButtonRelease-1>", self.stop_Capture)
        
        bt_goto_screen1 = Button(root, text="Go to Screen 1", font=font_text, command=self.gotoScreen1)
        bt_goto_screen1.grid(row=2, column=0, padx=5, pady=5)
        bt_show_data = Button(root,text = "Show data", font= font_text, command= self.showdata)
        bt_show_data.grid(row=3, column=0, padx=5, pady=5)
        
    def start_capture(self, event):
        self.start_x = event.x
        self.start_y = event.y
        global current_rectangle
        print("Start drawing rectangle")
        print("Start Possition: x=" + format(self.start_x) + " y=" + format(self.start_y)) 
        
    def curent_capture(self, event):
        self.current_x, self.current_y = event.x, event.y  
        global current_rectangle
        if self.current_rectangle:
            self.canvas.delete("rectangle")  
        x, y = self.start_x, self.start_y
        print("drawing rectangle")
        self.current_rectangle = self.canvas.create_rectangle(x, y, self.current_x, self.current_y,outline="red",width=2, tags="rectangle")   
              
    def stop_Capture(self, event):
        print("Stop drawing rectangle")
        self.current_rectangle = None
        self.stop_x = self.current_x
        self.stop_y = self.current_y
        print("self.start_x = " + format(self.start_x))
        print("self.start_y = " + format(self.start_y))
        print("self.current_x = " + format(self.stop_x))
        print("self.current_y = " + format(self.stop_y))
        # self.root.destroy() 
        self.gotoScreen1()     
        
    def showdata(self):
        print("Show data")
        print(self.data)
        
    def gotoScreen1(self):
        self.root.destroy() 
        screen1 = Toplevel(self.root.master)   
        self.data = [self.start_x,self.start_y,self.stop_x,self.stop_y]
        sc = Screen1(screen1)
        sc.set_value(self.data)
        
    def set_value(self,data):
        self.data = data
        self.update_screen()    
    
    def update_screen(self):
        print("Screen Updated")
    
def main():
    root = Tk()
    root.title("Main menu")
    root.geometry("400x300")
    app = Screen1(root)
    root.mainloop()

if __name__ == "__main__":
    main()