from colour_cls import *
from vectors import *
from typing import Self, List
import constants as const

G = const.G

class Object3:
    def __init__(self, position: Vector3, velocity: Vector3, name: str):
        self.pos = position
        self.vel = velocity
        self.trail: List[Vector3] = [self.pos for _ in range(const.trail_length)]
        self.name = name

    def addToTrail(self, trailIndex):
        self.trail[ trailIndex ] = self.pos# - tracking_pos

class Planet(Object3):
    def __init__(self, mass: float, radius: float, position: Vector3, velocity: Vector3,
                 name: str, colour: Colour, real: bool):
        super().__init__(position, velocity, name)
        self.m = mass
        self.r = radius
        self.colour = colour
        self.real = real

    def move(self, delta_time: float):
        self.pos = self.pos + self.vel * delta_time

    def experience_force(self, magnitude: float, direction: Vector3, delta_time: float):
        self.vel = self.vel + direction * (magnitude * delta_time / self.m)
    
    def accelerate(self, a: Vector3, dt: float):
        self.vel += a*dt

    def calc_distance(self, other: Self) -> float:
        distance = (self.pos - other.pos).mag

        #if distance < self.r + other.r:
        #    print(f"Collision between {self.name} and {other.name}")
        
        return distance
    
    def pull(self, other: Self, delta_time: float):
        distance = self.calc_distance(other)
        direction = (other.pos - self.pos).norm
        self.accelerate(a=direction*(G*other.m)/(distance*distance), dt=delta_time)
        #force = (G * self.m * other.m) / (2*distance**2)
        #other.experience_force(force, -direction, delta_time)

class COM(Object3):
    def __init__(self, position: Vector3, velocity: Vector3, planets: List[Planet], name: str):
        self.planets = planets
        self.calc_pos()
        super().__init__(position, velocity, name)
        self.prev_pos = self.pos

    def calc_pos(self):
        total = Vector3.zero
        mass = 0
        for obj in self.planets:
            total = total + obj.pos * obj.m
            mass = mass + obj.m
        self.pos = total / mass
    
    def calc_vel(self, dt: float):
        self.vel = (self.pos - self.prev_pos)/(dt*const.movement_updates_per_frame)