import pygame
from system_cls import *
from typing import List
import extract_nasa_data as nasa

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

def main():
    running = True
    clock = pygame.time.Clock()
    scroll = 0

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

    system = System3(objects, window, font, small_font, dt)

    following = None

    while running:
        clock.tick(frame_rate)
        window.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                scroll += event.y
                system.scroll_sf = 2**(scroll/2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    pos = pygame.mouse.get_pos()
                    system.centre += Vector2(pos[0] - 400, pos[1] - 400) / system.scroll_sf
                    following = None
                elif event.button == 2:
                    system.centre = Vector2(0,0)
                    following = None
                elif event.button == 1:
                    pos = pygame.mouse.get_pos()
                    vpos = Vector2(pos[0], pos[1])
                    for obj in system.objects:
                        if (obj.screenPos(system.com, system.sf, system.scroll_sf, system.centre)-vpos).mag \
                            < max(obj.screenRadius(system.scroll_sf), 5):
                            following = obj

        for _ in range(movement_updates_per_frame-1):
            system.move_all()
        if following:
            system.centre = (following.screenPos(system.com, system.sf, system.scroll_sf, Vector2(0,0)) - Vector2(400, 400)) / system.scroll_sf
        system.update_all()

        pygame.display.update()
    pygame.quit()

main()