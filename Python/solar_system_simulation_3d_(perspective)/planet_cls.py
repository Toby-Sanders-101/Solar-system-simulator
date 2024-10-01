from colour_cls import *
from vectors import *
from typing import Self, List

G = 6.67428e-11

offset = Vector2(400,400)

class Object3:
    def __init__(self, mass: float, radius: float, position: Vector3, velocity: Vector3,
                  name: str, colour: Colour):
        self.m = mass
        self.r = radius
        self.pos = position
        self.vel = velocity
        self.name = name
        self.colour = colour
        self.trail: List[Vector2] = []

    def move(self, delta_time: float):
        self.pos = self.pos + self.vel * delta_time

    def experience_force(self, magnitude: float, direction: Vector3, delta_time: float):
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