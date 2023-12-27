from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk ,ImageGrab , ImageDraw, EpsImagePlugin
from win32api import GetMonitorInfo, MonitorFromPoint
import pyperclip
import pyautogui
import keyboard
import io
white = (255, 255, 255)
rectangles = [(0, 0, 0, 0)]
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        global rectangles
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
        print("Start drawing rectangle")
        print("Start Possition: x=" + format(self.start_x) + " y=" + format(self.start_y))

    def draw_rectangle(self, event):
        current_x, current_y = event.x, event.y   
        if self.current_rectangle:
            self.canvas.delete(self.current_rectangle)
        x, y = self.start_x, self.start_y
        print("drawing rectangle")
        self.current_rectangle = self.canvas.create_rectangle(x, y, current_x, current_y,outline="red",width=2, tags="rectangle")           
            
    def stop_drawing(self, event):
        print("Stop drawing rectangle")
        self.current_rectangle = None
        self.rectangles.append((self.start_x, self.start_y, event.x, event.y))
        self.show_canvas(self.rectangles,0)                 
            
    def open_image(self):
        filetypes = (("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*"))
        # lbn_img = Label(root,image=self.image_ref)
        # lbn_img.place(x= 0,y = 2)
        # self.image_ref = ImageTk.PhotoImage(img)
        global filepath
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            global img_height, img_width, img
            img = Image.open(filepath)
            img_width, img_height = img.size
            print(img_height)
            print(canvas_height)
            if(img_height > canvas_height):
                global zoom_factor
                zoom_factor = (canvas_height - taskpar_height) / img_height
                print(zoom_factor)               
                img_width = int(img_width * zoom_factor)
                img_height = int(img_height * zoom_factor)
                print("Width New: " + format(img_width))
                print("Height New: " + format(img_height))
                zoomed_image = img.resize((img_width, img_height), Image.BICUBIC)
                img = zoomed_image
                
            self.image_ref = ImageTk.PhotoImage(img)
            # self.canvas.create_image(0, 0, anchor=NW, image=self.image_ref) 
            self.rectangles = []              
            self.show_canvas(self.rectangles,1)               
        
    def on_key_press(self,event):
        if event.name == 'z' and keyboard.is_pressed('ctrl'):
            i_lenTuple = len(self.rectangles)
            if i_lenTuple > 0:
                tempTuple = self.rectangles[:-1]
                self.rectangles = tempTuple
                self.show_canvas(self.rectangles,0)
                print("ctrl + z")
    
    def show_canvas(self,rectangles,mode):
        print("Show rectangle")
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_ref) 
        if mode == 0:            
            for rectangle in rectangles:
                print("Show rectangle Original"+ format(rectangle))
                self.canvas.create_rectangle(rectangle,outline="red",width=2)  
                                  
    # def save_canvas(self):
    #     y_axis = 45
    #     print("Zoom factor: " + format(zoom_factor))
    #     path_file = r"D:\Project\AutoCapture\img\filename.png"
    #     image = pyautogui.screenshot(region=(2, y_axis, img_width-2, img_height-3))
    #     img_widthOut = int(img_width / zoom_factor)
    #     img_heightOut = int(img_height / zoom_factor)
    #     img_output = image.resize((img_widthOut, img_heightOut), Image.BICUBIC)
    #     img_output.save(path_file)
    #     print("Canvas saved ")         
    def save_canvas(self):
        output_path = "D:\Project\AutoCapture\img\output.png"
        image = Image.open(filepath)
        draw = ImageDraw.Draw(image)
        # draw.rectangle((x, y, x + width, y + height), outline="red", width=2)
        temptuple = self.rectangles
        # if img_height > canvas_height
            
        for m_tuple in temptuple:
            if img_height > canvas_height:
                m_tuple = tuple([ value / zoom_factor for value in m_tuple])
            draw.rectangle(m_tuple, outline="red", width=2)
            image.save(output_path)
            print("Show rectangle new"+ format(m_tuple))
            
        print("Saved file")
        
        
                 
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

my_tuple = [(5, 3),(10,20)]

by_five = tuple(5 * elem for elem in my_tuple)

print(by_five)  # 👉️ (25, 15)


app = PaintApp(root)
# canvasrec= Canvas(root, width=canvas_width, height=canvas_height)
# rectangles = [(681, 218, 815, 368),
#                            (982, 480, 1048, 559),
#                            (656, 514, 705, 583),
#                            (909, 544, 1030, 666),
#                            (510, 492, 585, 547),
#                            (829, 491, 878, 548)]
# for i in rectangles:
#     print("Show rectangle"+ format(i))
#     canvasrec.create_rectangle(i,outline="red",width=3)
root.mainloop()