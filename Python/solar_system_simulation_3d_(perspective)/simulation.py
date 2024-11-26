import pygame
from system_cls import *
from typing import List
import extract_nasa_data as nasa
import constants as const

pygame.init()

print("")

width, height = const.width, const.height

frame_rate = const.frame_rate
dt = 10**const.log10_init_dt
movement_updates_per_frame = const.movement_updates_per_frame
speed_multiplier = frame_rate * dt * movement_updates_per_frame
print(f"The simulation is running at:\n* {frame_rate}Hz (graphics)\n* {movement_updates_per_frame*frame_rate}Hz (physics)\n")

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar system simulator")

font = pygame.font.SysFont("comicsansms", 18)
small_font = pygame.font.SysFont("comicsansms", 14)

class Main:
    def __init__(self):
        self.cam = Camera(window, font, small_font)
        self.new_dt = self.dt = dt
        self.running = True
        self.clock = pygame.time.Clock()
        self.scroll = const.init_scroll
        self.cam.scale = 2**(self.scroll/2)
        self.tkwindow: Window = None

        self.objects: List[Planet] = []
        self.real_planets: List[Planet] = []

        self.array = nasa.read_all_today()
        for dict in self.array:
            name = dict["name"]
            if name in predefined_colours.keys():
                colour = predefined_colours[name]
            else:
                colour = Colour()
            planet = Planet(mass=dict["m"], radius=dict["r"],
                         position=Vector3(dict["x"], dict["y"], dict["z"]),
                         velocity=Vector3(dict["vx"], dict["vy"], dict["vz"]),
                         name=name, colour=colour, real=dict["real_planet?"])
            self.objects.append(planet)
            if planet.real:
                self.real_planets.append(planet)

        print(f"\nStarting the simulation with {len(self.objects)} bodies")
        self.system = System3(self.real_planets, self.objects, self.dt, self.cam)

    def start(self):
        while self.running:
            self.clock.tick(frame_rate)
            window.fill(const.background_colour)
            self.update()
            pygame.display.update()
        pygame.quit()


    def update(self):
        self.takeInputs()
        self.dt = self.system.dt = self.new_dt
        for _ in range(movement_updates_per_frame-1):
            self.system.move_all()
        self.system.update_all()
    
    def takeInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll += event.y
                if self.scroll > const.scroll_max:
                    self.scroll = const.scroll_max
                elif self.scroll < const.scroll_min:
                    self.scroll = const.scroll_min
                self.tkwindow.scale.set(self.scroll)
                self.cam.scale = 2**(self.scroll/2)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 or event.button == 1:
                    self.prev_mouse_pos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            self.cam.move(Vector3(6/self.cam.scale, 0, 0))
        if keys[pygame.K_RIGHT]:
            self.cam.move(Vector3(-6/self.cam.scale, 0, 0))
        if keys[pygame.K_UP]:
            self.cam.move(Vector3(0, 6/self.cam.scale, 0))
        if keys[pygame.K_DOWN]:
            self.cam.move(Vector3(0, -6/self.cam.scale, 0))
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            temp = pygame.mouse.get_pos()
            self.cam.move(Vector3((self.prev_mouse_pos[0]-temp[0])/self.cam.scale, (self.prev_mouse_pos[1]-temp[1])/self.cam.scale, 0))
            self.prev_mouse_pos = temp
        if mouse[1]:
            temp = pygame.mouse.get_pos()
            temp = Vector2(temp[0], temp[1])
            closest = 1000000
            for obj in self.real_planets:
                xy, _ = self.cam.pos_to_xy_z(obj.pos)
                dist = (xy-temp).mag
                if dist < const.radius_to_pixels(obj.r, self.cam.scale) + const.clicking_uncertainty and dist < closest:
                    if obj != self.system.tracking:
                        self.cam.reset_pos()
                    self.system.tracking = obj
                    closest = dist
            self.tkwindow.new_focus(self.system.tracking.name)
        if mouse[2]:
            temp = pygame.mouse.get_pos()
            self.cam.rotate(Vector3(self.prev_mouse_pos[1]-temp[1], temp[0]-self.prev_mouse_pos[0], 0)/5)
            self.prev_mouse_pos = temp

from window import *

main = Main()
tkwindow = Window()
main.tkwindow = tkwindow
tkwindow.main = main
main.start()