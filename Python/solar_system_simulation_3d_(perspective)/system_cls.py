from typing import List
import datetime
from vectors import *
from colour_cls import *
from planet_cls import *
from camera import Camera

class System3:
    TRAIL_LENGTH = const.trail_length

    def __init__(self, real_planets: List[Planet], objects: List[Planet], dt, cam: Camera):
        self.com = COM(Vector3.zero, Vector3.zero, objects, "com")
        self.dt = dt
        self.real_planets = real_planets
        self.objects = objects

        self.it = 1
        self.time = datetime.datetime.today()

        self.tracking: Object3 = self.com
        self.trailIndex = 0

        self.cam = cam
        cam.planets = objects
        cam.real_planets = real_planets

    def move_all(self):
        for body in self.objects:
            for obj in self.objects:
                if obj != body:
                    obj.pull(body, self.dt)
            body.move(self.dt)
        self.time = self.time + datetime.timedelta(seconds=self.dt)

    def addToTrails(self):
        for body in self.objects:
            body.addToTrail(self.trailIndex)
        self.com.addToTrail(self.trailIndex)
        self.trailIndex += 1
        self.trailIndex %= self.TRAIL_LENGTH

    def switchToCOM(self):
        if self.tracking != self.com:
            self.tracking = self.com
            self.cam.reset_pos()

    def update_all(self):
        self.com.prev_pos = self.com.pos

        self.move_all()

        self.com.calc_pos()
        self.com.calc_vel(self.dt)

        self.cam.tracking = self.tracking

        self.cam.display(self.time)
        if self.it % 2 == 0:
            self.addToTrails()
        self.it += 1

