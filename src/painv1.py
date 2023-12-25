from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk ,ImageGrab , ImageDraw, EpsImagePlugin
from win32api import GetMonitorInfo, MonitorFromPoint
import pyperclip
import pyautogui
import keyboard
white = (255, 255, 255)
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.rectangles = []
        self.current_rectangle = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.image_ref = None
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        keyboard.on_press(self.on_key_press)
        global count 
        self.menu = Menu(root)
        self.root.config(menu=self.menu)

        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_canvas)

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw_rectangle(self, event):
        if self.current_rectangle:
            self.canvas.delete(self.current_rectangle)
        x, y = self.start_x, self.start_y
        current_x, current_y = event.x, event.y
        self.current_rectangle = self.canvas.create_rectangle(x, y, current_x, current_y,outline="red",width=3, tags="rectangle")

    def stop_drawing(self, event):
        self.current_rectangle = None
        # self.rectangles.append((self.start_x, self.start_y, event.x, event.y))
        print(self.rectangles)
        
    def on_key_press(self,event):
        if(event.name == 'z' and keyboard.is_pressed('ctrl')):
            # self.canvas.delete("rectangle" +str(count-1))
            print("ctrl + z")
    
    def open_image(self):
        filetypes = (("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*"))
        # lbn_img = Label(root,image=self.image_ref)
        # lbn_img.place(x= 0,y = 2)
        # self.image_ref = ImageTk.PhotoImage(img)
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            global img_height, img_width
            img = Image.open(filepath)
            img_width, img_height = img.size
            print(img_height)
            print(canvas_height)
            if(img_height > canvas_height):
                zoom_factor = (canvas_height - taskpar_height) / img_height
                print(zoom_factor)               
                img_width = int(img_width * zoom_factor)
                img_height = int(img_height * zoom_factor)
                print("Width New: " + format(img_width))
                print("Height New: " + format(img_height))
                zoomed_image = img.resize((img_width, img_height), Image.BICUBIC)
                img = zoomed_image
                
            self.image_ref = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_ref)                              
            
            
    def save_canvas(self):
         y_axis = 45
         path_file = r"D:\Project\AutoCapture\img\filename.png"
         image = pyautogui.screenshot(region=(2, y_axis, img_width-2, img_height-3))
         image.save(path_file)
         print("Canvas saved ")         
                  
root = Tk()
# root.attributes('-fullscreen', True)
root.state("zoomed")
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
canvas_width = work_area[2]
canvas_height = work_area[3]
taskpar_height = monitor_area[3]-work_area[3]
print("The taskbar height is {}.".format(monitor_area[3]-work_area[3]))
# print("The screen full is " + format(monitor_area) )
# print("The work_area full is " + format(work_area) )
# print("The worksSpace height is " + str(canvas_height))
# print("The worksSpace width is " + str(canvas_width))


app = PaintApp(root)

root.mainloop()