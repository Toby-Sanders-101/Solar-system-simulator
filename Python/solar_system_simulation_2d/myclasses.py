import numpy as np
from typing import Self, List
import random
import pygame

class Colour:
    def __init__(self, r=-1, g=-1, b=-1, alpha=1):
        if r == -1 and g == -1 and b == -1:
            self.r = random.randint(0, 255)
            self.g = random.randint(0, 255)
            self.b = random.randint(0, 255)
            self.alpha = alpha
        else:
            if r > 255:
                r = 255
            if r < 0:
                r = 0
            self.r = int(r)

            if g > 255:
                g = 255
            if g < 0:
                g = 0
            self.g = int(g)

            if b > 255:
                b = 255
            if b < 0:
                b = 0
            self.b = int(b)

            if alpha > 1:
                alpha = 1
            if alpha < 0:
                alpha = 0
            self.alpha = alpha
    
    @property
    def tuple(self) -> tuple:
        return (self.r, self.g, self.b, self.alpha)

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, b: Self) -> Self:
        return Vector2(self.x+b.x, self.y+b.y)
    
    def __sub__(self, b: Self) -> Self:
        return Vector2(self.x-b.x, self.y-b.y)
    
    def __mul__(self, k: float) -> Self:
        return Vector2(self.x * k, self.y * k)
    
    def __truediv__(self, k: float) -> Self:
        return Vector2(self.x / k, self.y / k)
    
    @property
    def mag(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)

    @property
    def norm(self) -> Self:
        return self / self.mag
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y)
    
G = 6.67428e-11

#sf = 2e-9

offset = Vector2(400, 400)

class Object2:
    def __init__(self, mass: float, radius: float, position: Vector2, velocity: Vector2,
                  name: str, colour: Colour):
        self.m = mass
        self.r = radius
        self.pos = position
        self.vel = velocity
        self.name = name
        self.colour = colour
        print(self.name, self.m)
        print(self.pos.tuple)
        print(self.vel.tuple)
        print("-------------")

    def move(self, delta_time: float):
        self.pos = self.pos + self.vel * delta_time

    def experience_force(self, magnitude: float, direction: Vector2, delta_time: float):
        self.vel = self.vel + direction * (magnitude * delta_time / self.m)
    
    def calc_distance(self, other: Self) -> float:
        distance = (self.pos - other.pos).mag

        if distance < self.r + other.r:
            print(f"Collision between {self.name} and {other.name}")
        
        return distance
    
    def pull(self, other: Self, delta_time: float):
        distance = self.calc_distance(other)
        force = (G * self.m * other.m) / (distance**2)
        direction = (self.pos - other.pos).norm
        other.experience_force(force, direction, delta_time)


    def draw(self, window, font, small_font, com, com_vel, sf):
        radius = ((np.log10(self.r) / 3.5) ** 1.5) * 3#sf * self.r * 1000
        coordinates = (self.pos - com) * sf + offset
        pygame.draw.circle(window, self.colour.tuple, coordinates.tuple, radius)
        name_text = font.render(self.name, 1, self.colour.tuple)
        window.blit(name_text, (coordinates + Vector2(radius, radius)).tuple)
        speed_text = small_font.render(str(round((self.vel-com_vel).mag/1000, 2)) + " km/s", 1, self.colour.tuple)
        window.blit(speed_text, (coordinates + Vector2(radius, radius+30)).tuple)

class System2:
    COM_ARR_COUNT = 8

    def __init__(self, objects: List[Object2], window, font, small_font, dt):
        self.com = Vector2(0,0)
        self.com_vel = Vector2(0,0)
        self.com_arr: List[Vector2] = []
        self.sf = 1
        self.window = window
        self.font = font
        self.small_font = small_font
        self.dt = dt
        self.objects = objects
        self.calc_com()
        self.com_arr = [self.com for _ in range(self.COM_ARR_COUNT)]
        self.calc_sf()
        print(self.sf)
    
    def calc_com(self):
        total = Vector2(0,0)
        mass = 0
        for obj in self.objects:
            total = total + obj.pos * obj.m
            mass = mass + obj.m
        total = total / mass
        self.com = total
        #print(total.tuple)
    
    def calc_com_vel(self):
        self.com_vel = (self.com - self.com_arr.pop(0)) / (self.COM_ARR_COUNT * self.dt)
        self.com_arr.append(self.com)

    def calc_sf(self):
        x = 0
        y = 0
        for obj in self.objects:
            x = max(x, abs(obj.pos.x - self.com.x))
            y = max(y, abs(obj.pos.y - self.com.y))
        boundary = max(x,y)
        self.sf = 300 / boundary
    
    def update_all(self):
        self.calc_com()
        self.calc_com_vel()
        #self.calc_sf()
        for body in self.objects:
            for obj in self.objects:
                if obj != body:
                    obj.pull(body, self.dt)
            body.move(self.dt)
            body.draw(self.window, self.font, self.small_font, self.com, self.com_vel, self.sf)

