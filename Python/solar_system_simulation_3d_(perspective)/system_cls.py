from typing import List
import datetime
from vectors import *
from colour_cls import *
from planet_cls import *
from camera import Camera

class System3:
    COM_ARR_COUNT = 8

    def __init__(self, objects: List[Object3], dt, cam: Camera):
        self.com = Vector3(0,0,0)
        self.com_vel = Vector3(0,0,0)
        self.com_arr: List[Vector3] = []
        self.dt = dt
        self.objects = objects
        self.calc_com()
        self.com_arr = [self.com for _ in range(self.COM_ARR_COUNT)]

        self.scroll_sf = 1
        self.it = 0
        self.time = datetime.datetime.today()
        self.centre = Vector2(0, 0)

        self.cam = cam
        cam.planets = objects
    
    def calc_com(self):
        total = Vector3(0,0,0)
        mass = 0
        for obj in self.objects:
            total = total + obj.pos * obj.m
            mass = mass + obj.m
        total = total / mass
        self.com = total
    
    def calc_com_vel(self):
        self.com_vel = (self.com - self.com_arr.pop(0)) / (self.COM_ARR_COUNT * self.dt)
        self.com_arr.append(self.com)
    
    def move_all(self):
        self.calc_com()
        self.calc_com_vel()
        for body in self.objects:
            for obj in self.objects:
                if obj != body:
                    obj.pull(body, self.dt)
            body.move(self.dt)
        self.time = self.time + datetime.timedelta(seconds=self.dt)

    def update_all(self):
        self.move_all()
        self.cam.display(self.com, self.com_vel, self.time)

