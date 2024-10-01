import pygame
from system_cls import *
from typing import List
import extract_nasa_data as nasa
import time

#TODO:
###make colours different
###change centre
#show perspective
#add more objects (only visible if close enough)
###show dates
#make relativistic
#use compiled language

pygame.init()

print("")
print("")

width, height = 800, 800

frame_rate = 15
dt = 2000
movement_updates_per_frame = 24
speed_multiplier = frame_rate * dt * movement_updates_per_frame
print(f"The simulation is running at:\n* {frame_rate}Hz (graphics)\n* {movement_updates_per_frame*frame_rate}Hz (physics)\n* {speed_multiplier//(60*60*24)} simulation days per real second\n\n")

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar system simulator")

font = pygame.font.SysFont("comicsansms", 18)
small_font = pygame.font.SysFont("comicsansms", 14)

cam = Camera(window, font, small_font)

def main():
    running = True
    clock = pygame.time.Clock()
    scroll = -69
    cam.scale = 2**(scroll/2)

    objects: List[Object3] = []

    array = nasa.read_all_today()
    for dict in array:
        name = dict["name"]
        if name == "earth":
            colour = Colour(0,0,200)
        elif name == "sun":
            colour = Colour(200,200,0)
        elif name == "moon":
            colour = Colour(80,80,80)
        elif name == "mars":
            colour = Colour(200,80,30)
        elif name == "jupiter":
            colour = Colour(200,0,100)
        else:
            colour = Colour()
        planet = Object3(mass=dict["m"], radius=dict["r"],
                         position=Vector3(dict["x"], dict["y"], dict["z"]),
                         velocity=Vector3(dict["vx"], dict["vy"], dict["vz"]),
                         name=name, colour=colour)
        objects.append(planet)

    system = System3(objects, dt, cam)

    while running:
        clock.tick(frame_rate)
        window.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEWHEEL:
                scroll += event.y
                cam.scale = 2**(scroll/2)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 or event.button == 1:
                    prev_mouse_pos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            cam.move(Vector3(-4/cam.scale, 0, 0))
        if keys[pygame.K_RIGHT]:
            cam.move(Vector3(4/cam.scale, 0, 0))
        if keys[pygame.K_UP]:
            cam.move(Vector3(0, -4/cam.scale, 0))
        if keys[pygame.K_DOWN]:
            cam.move(Vector3(0, 4/cam.scale, 0))
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            temp = pygame.mouse.get_pos()
            cam.move(Vector3((prev_mouse_pos[0]-temp[0])/cam.scale, (prev_mouse_pos[1]-temp[1])/cam.scale, 0))
            prev_mouse_pos = temp
        if mouse[2]:
            temp = pygame.mouse.get_pos()
            cam.rotate(Vector3((prev_mouse_pos[0]-temp[0]), (prev_mouse_pos[1]-temp[1]), 0))
            prev_mouse_pos = temp


        for _ in range(movement_updates_per_frame-1):
            system.move_all()
        system.update_all()

        pygame.display.update()
    pygame.quit()

main()