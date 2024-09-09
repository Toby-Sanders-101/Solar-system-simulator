import pygame
from myclasses import *
from typing import List
import extract_nasa_data as nasa

pygame.init()

width, height = 800, 800

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar system simulator")

font = pygame.font.SysFont("comicsansms", 18)
small_font = pygame.font.SysFont("comicsansms", 14)

def main():
    running = True
    clock = pygame.time.Clock()

    objects: List[Object2] = []

    array = nasa.read_all_today()
    for dict in array:
        name = dict["name"]
        if name == "earth":
            colour = Colour(0,0,200)
        elif name == "sun":
            colour = Colour(155,155,0)
        elif name == "moon":
            colour = Colour(80,80,80)
        else:
            colour = Colour()
        planet = Object2(mass=dict["m"], radius=dict["r"],
                         position=Vector2(dict["x"], dict["y"]),
                         velocity=Vector2(dict["vx"], dict["vy"]),
                         name=name, colour=colour)
        objects.append(planet)

    #earth = Object2(mass=5.972e24, radius=6378137, 
    #                position=Vector2(147095e6, 0), velocity=Vector2(0, 30290),
    #                name="earth", colour=Colour(0,0,200))

    #sun = Object2(mass=1.9884e30, radius=695700000,
    #              position=Vector2(0, 0), velocity=Vector2(0, 0),
    #              name="sun", colour=Colour(155,155,0))
    

    system = System2(objects, window, font, small_font, dt=20000)

    while running:
        clock.tick(60)
        window.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #dt = 10000

        #for body in objects:
        #    for obj in objects:
        #        if obj != body:
        #            obj.pull(body, dt)
        #    body.move(dt)
        #    body.draw(window, font, small_font)

        system.update_all()

        #sun.pull(earth, dt)
        #earth.pull(sun, dt)

        #earth.move(dt)
        #sun.move(dt)

        #earth.draw(window, font, small_font)
        #sun.draw(window, font, small_font)

        pygame.display.update()
    pygame.quit()

main()