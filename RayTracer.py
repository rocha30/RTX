import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from figures import *
from lights import *
from Material import *

width = 100
height = 100

# pygame.init() 
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)


#Spheres 
rend.scene.append(Sphere(position=[1, -1, -5], radius=1.0, material = red_material))
# rend.scene.append(Sphere(position=[0, 0, -7], radius=0.5, material = green_material))


# Luces
rend.lights.append(AmbientLight())
rend.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity = 1))



isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
    
    rend.glRender()
    clock.tick(60)


GenerateBMP('output.bmp', width, height, 3, rend.frameBuffer)

pygame.quit()