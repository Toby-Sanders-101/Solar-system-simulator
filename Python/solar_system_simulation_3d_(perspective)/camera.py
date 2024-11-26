from vectors import *
from colour_cls import *
from planet_cls import *
from typing import List
from matrices import *
import bisect
from dataclasses import dataclass
import pygame
import constants as const

@dataclass
class PlanetToDraw:
    pos: Vector2
    name: str
    col: Colour
    speed: str
    radius: float
    trail: List[Vector3]

class Camera:
    TRAIL_LENGTH = const.trail_length

    def __init__(self, window, font, small_font):
        self.position = Vector3.zero
        self.rotation = Vector3.zero
        self.scale = 1
        self.screen_size = Vector2(const.width,const.height)
        self.window = window
        self.font = font
        self.small_font = small_font
        self.real_planets: List[Planet]
        self.planets: List[Planet]
        self.tracking: Object3 = None

    def move(self, movement: Vector3):
        self.position += movement
    
    def rotate(self, angle: Vector3):
        self.rotation += angle
    
    def reset_pos(self):
        self.position = Vector3.zero

    def drawLine(self, label, direction, rotmat):
        coordinates1 = ((multiply(rotmat, -direction).asVector3-self.position).asVector2 * self.scale + self.screen_size / 2)
        coordinates2 = ((multiply(rotmat, direction).asVector3-self.position).asVector2 * self.scale + self.screen_size / 2)
        coordinates3 = ((multiply(rotmat, direction).asVector3-self.position).asVector2.norm * 350 + self.screen_size / 2)
        pygame.draw.line(self.window, const.font_colour, coordinates1.tuple, coordinates2.tuple)
        name_text = self.font.render(label, 1, const.font_colour)
        self.window.blit(name_text, coordinates3.tuple)

    def pos_to_xy_z(self, pos: Vector3, rotmat: Matrix | None = None):
        if rotmat is None:
            rotmat = multiply(rotationmatrix3x3("z", self.rotation.z), rotationmatrix3x3("y", self.rotation.y), rotationmatrix3x3("x", self.rotation.x))
        coords = multiply(rotmat, pos-self.tracking.pos).asVector3-self.position
        return coords.asVector2 * self.scale + self.screen_size/2, coords.mag

    def display(self, time):

        self.orderedList: List[tuple[float, PlanetToDraw]] = []

        rotmat = multiply(rotationmatrix3x3("z", self.rotation.z), rotationmatrix3x3("y", self.rotation.y), rotationmatrix3x3("x", self.rotation.x))
        self.drawLine("x", Vector3(500/self.scale,0,0), rotmat)
        self.drawLine("y", Vector3(0,500/self.scale,0), rotmat)
        self.drawLine("z", Vector3(0,0,500/self.scale), rotmat)
        if self.scale >= const.scale_min_for_vis_moons:
            for planet in self.planets:
                xy, z = self.pos_to_xy_z(planet.pos, rotmat)
                radius = const.radius_to_pixels(planet.r, self.scale)
                bisect.insort(self.orderedList, (-z, PlanetToDraw(pos=xy, name=planet.name, col=planet.colour, 
                                                                  speed=str(round((planet.vel-self.tracking.vel).mag/1000, 2)) + " km/s", radius=radius, trail=planet.trail)))
        else:
            for planet in self.real_planets:
                xy, z = self.pos_to_xy_z(planet.pos, rotmat)
                radius = const.radius_to_pixels(planet.r, self.scale)
                bisect.insort(self.orderedList, (-z, PlanetToDraw(pos=xy, name=planet.name, col=planet.colour, 
                                                                  speed=str(round((planet.vel-self.tracking.vel).mag/1000, 2)) + " km/s", radius=radius, trail=planet.trail)))
        
        for _, planet in self.orderedList:
            pygame.draw.circle(self.window, planet.col.tuple, planet.pos.tuple, planet.radius)
            for index in range(self.TRAIL_LENGTH):
                point, _ = self.pos_to_xy_z(planet.trail[index]-self.tracking.trail[index]+self.tracking.pos, rotmat)
                #point = (multiply(rotmat, point).asVector3-self.position).asVector2 * self.scale + self.screen_size/2
                pygame.draw.circle(self.window, planet.col.tuple, point.tuple, 1)
            name_text = self.font.render(planet.name, 1, planet.col.tuple)
            self.window.blit(name_text, (planet.pos + Vector2(planet.radius, planet.radius)).tuple)
            speed_text = self.small_font.render(planet.speed, 1, planet.col.tuple)
            self.window.blit(speed_text, (planet.pos + Vector2(planet.radius, planet.radius+30)).tuple)
        
        time_text = self.font.render(str(time.strftime(f"%d/%m/%Y")), 1, const.font_colour)
        self.window.blit(time_text, (336, 10))