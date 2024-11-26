from tkinter import *
import threading
from typing import TYPE_CHECKING
import math
import constants as const
from PIL import Image as PImage
from PIL import ImageTk as PImageTk

if TYPE_CHECKING:
    from simulation import Main

w = const.window_width

class Window:
    def __init__(self):
        thread = threading.Thread(target=self.start, args=(1,), daemon=True)
        thread.start()
        self.main: Main = None
        self.rate = const.frame_rate * const.movement_updates_per_frame
        self.time_direction = 1
        self.focus = "com"
    
    def start(self, n):
        self.root = Tk()
        self.root.title("Options and data")

        self.scale = Scale(self.root, from_=const.scroll_min, to=const.scroll_max, orient=HORIZONTAL, resolution=1, command=self.scaleChange, length=w)
        if self.main != None:
            self.scale.set(self.main.scroll)
        else:
            self.scale.set(const.init_scroll)
        self.scale.pack()

        self.dt = Scale(self.root, from_=0, to=5, orient=HORIZONTAL, resolution=0.02, command=self.dtChange, length=w)
        self.time_speed_lbl = Label(self.root)
        self.physics_speed_lbl = Label(self.root)
        self.time_direction_btn = Button(self.root, command=self.reverseTime)
        self.com_mode_btn = Button(self.root, command=self.switchToCOM, text="Switch to COM mode")
        self.image = Label(self.root)
        self.image_ref = None
        self.data_lbl = Label(self.root, background="white", wraplength=w)

        if self.main != None:
            self.dt.set(math.log10(self.main.dt))
            self.time_speed_lbl["text"] = f"{round(self.rate * self.main.dt/(60*60*24),3)} simulation days per real second"
            self.physics_speed_lbl["text"] = f"{const.float_to_standard_form(self.main.dt)} simulation seconds between physics frames"
            self.time_direction = 1 if self.main.dt >= 0 else -1
            self.time_direction_btn["text"] = "Switch to backwards time?" if self.time_direction == 1 else "Switch to forwards time?"
        else:
            self.dt.set(const.log10_init_dt)
            self.time_speed_lbl["text"] = f"{round(self.rate * 10**const.log10_init_dt/(60*60*24),2)} simulation days per real second"
            self.physics_speed_lbl["text"] = f"{const.float_to_standard_form(10**const.log10_init_dt)} simulation seconds between physics frames"
            self.time_direction_btn["text"] = "Switch to backwards time?"
            
        self.dt.pack()
        self.time_speed_lbl.pack()
        self.physics_speed_lbl.pack()
        self.time_direction_btn.pack()
        self.com_mode_btn.pack()
        self.new_focus(self.focus)

        self.root.mainloop()
        self.start(n)

    def scaleChange(self, v):
        v = int(v)
        self.main.scroll = v
        self.main.cam.scale = 2**(v/2)
    
    def dtChange(self, v):
        v = float(v)
        dt = 10**v
        self.main.new_dt = dt * self.time_direction
        self.time_speed_lbl["text"] = f"{round(self.rate * dt/(60*60*24),2)} simulation days per real second"
        self.physics_speed_lbl["text"] = f"{const.float_to_standard_form(dt)} simulation seconds between physics frames"

    def reverseTime(self):
        self.main.new_dt *= -1
        self.time_direction *= -1
        self.time_direction_btn["text"] = "Switch to backwards time?" if self.time_direction == 1 else "Switch to forwards time?"
    
    def switchToCOM(self):
        self.main.system.switchToCOM()
        self.new_focus("com")
    
    def fetch_data(self, planet: str) -> str:
        file = const.base_path + "data_sheets/" + planet + ".txt"
        try:
            with open(file, "r") as f:
                text = f.read()
            return text
        except:
            print("no file found at", file)
            return ""

    def fetch_image(self, planet: str) -> PImageTk.PhotoImage:
        file = const.base_path + "images/" + planet + ".webp"
        try:
            image = PImage.open(file)
            h = int(w * (image.height / image.width))
            image = image.resize((w,h), PImage.Resampling.LANCZOS)
            img = PImageTk.PhotoImage(image)
            return img
        except:
            print("no file found at", file)
            return None


    def new_focus(self, planet: str):
        self.focus = planet
        data: str
        image: PImageTk.PhotoImage

        if planet == "com":
            data = ""
            image = None
        else:
            data = self.fetch_data(planet)
            image = self.fetch_image(planet)
        
        if image is None:
            self.image.pack_forget()
        else:
            self.image.configure(image=image)
            self.image_ref = image
            self.image.pack()
        
        self.data_lbl["text"] = data
        if data == "":
            self.data_lbl.pack_forget()
        else:
            self.data_lbl.pack()