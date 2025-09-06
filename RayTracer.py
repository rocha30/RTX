import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from BMPTexture import BMPTexture
from figures import *
from lights import *
from Material import *

width = 255
height = 255


screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.envMap = BMPTexture('fondo.bmp')

rend.scene.append(Sphere(position=[0, 0, -5], radius=0.8, material = red_material))
#Spheres 
rend.scene.append(Sphere(position=[2, 0, -5], radius=0.5, material = mirror_material))


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