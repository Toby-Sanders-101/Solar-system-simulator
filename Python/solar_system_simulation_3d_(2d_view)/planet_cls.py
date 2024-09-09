from colour_cls import *
from vectors import *
from typing import Self, List
import pygame

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

    def draw(self, window, font, small_font, com, com_vel, sf, scroll_sf, it, centre):
        for dot in self.trail:
            r = max(scroll_sf / 4, 1)
            x = (dot) * sf * scroll_sf + offset - (centre * scroll_sf)
            pygame.draw.circle(window, self.colour.tuple, x.tuple, r)
        if it % 15 == 0:
            self.trail.append(self.pos.asVector2 - com)
            if len(self.trail) > 30:
                self.trail.pop(0)
        radius = self.screenRadius(scroll_sf)
        coordinates = self.screenPos(com, sf, scroll_sf, centre)
        pygame.draw.circle(window, self.colour.tuple, coordinates.tuple, radius)
        name_text = font.render(self.name, 1, self.colour.tuple)
        window.blit(name_text, (coordinates + Vector2(radius, radius)).tuple)
        speed_text = small_font.render(str(round((self.vel-com_vel).mag/1000, 2)) + " km/s", 1, self.colour.tuple)
        window.blit(speed_text, (coordinates + Vector2(radius, radius+30)).tuple)
    
    def screenPos(self, com, sf, scroll_sf, centre) -> Vector2:
        return ((self.pos.asVector2 - com) * sf) * scroll_sf + offset - (centre * scroll_sf)
    
    def screenRadius(self, scroll_sf) -> float:
        return max(((np.log10(self.r) / 3.5) ** 1.4) * scroll_sf, 2)