from vectors import *
from colour_cls import *
from planet_cls import *
from typing import List
from matrices import *
import bisect
from dataclasses import dataclass
import numpy
import pygame

@dataclass
class PlanetToDraw:
    pos: Vector2
    name: str
    col: Colour
    speed: str
    radius: float

class Camera:
    def __init__(self, window, font, small_font):
        self.position = Vector3(0,0,0)
        self.rotation = Vector3(0,0,0)
        self.scale = 1
        self.screen_size = Vector2(800,800)
        self.viewing_angle = 60
        self.window = window
        self.font = font
        self.small_font = small_font
        self.planets : List[Object3]

    def move(self, movement: Vector3):
        self.position += multiply(rotationmatrix3x3("x", self.rotation.x), rotationmatrix3x3("y", self.rotation.y), rotationmatrix3x3("z", self.rotation.z), movement).asVector3
    
    def rotate(self, angle: Vector3):
        self.rotation += angle
    
    def display(self, com, com_vel, time):

        orderedList : List[Object3] = []

        rotmat = multiply(rotationmatrix3x3("x", self.rotation.x), rotationmatrix3x3("y", self.rotation.y), rotationmatrix3x3("z", self.rotation.z))
        for planet in self.planets:
            coordinates = planet.pos - com - self.position
            coordinates = multiply(rotmat, coordinates).asVector3
            xy = coordinates.asVector2 * self.scale + self.screen_size / 2
            z = coordinates.mag
            radius = numpy.sqrt(numpy.sqrt(planet.r) * self.scale) * 1e4
            bisect.insort(orderedList, (1/z, PlanetToDraw(pos=xy, name=planet.name, col=planet.colour, speed=str(round((planet.vel-com_vel).mag/1000, 2)) + " km/s", radius=radius)))

        for _, planet in orderedList:
            pygame.draw.circle(self.window, planet.col.tuple, planet.pos.tuple, planet.radius)
            name_text = self.font.render(planet.name, 1, planet.col.tuple)
            self.window.blit(name_text, (planet.pos + Vector2(planet.radius, planet.radius)).tuple)
            speed_text = self.small_font.render(planet.speed, 1, planet.col.tuple)
            self.window.blit(speed_text, (planet.pos + Vector2(planet.radius, planet.radius+30)).tuple)
        
        time_text = self.font.render(str(time.strftime(f"%d/%m/%Y")), 1, (0,0,0))
        self.window.blit(time_text, (336, 10))