import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from BMPTexture import BMPTexture
from figures import *
from lights import *
from Material import *

width = 720
height = 720


screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.envMap = BMPTexture('Fondo.bmp')

#Spheres 
rend.scene.append(Sphere(position=[-3, 2, -5], radius=1, material = matte_red))
rend.scene.append(Sphere(position=[0, 2, -5], radius=1, material = glossy_blue))
rend.scene.append(Sphere(position=[3, 2, -5], radius=1, material = polished_gold))
rend.scene.append(Sphere(position=[-3, -2, -5], radius=1, material = lacquer_red))
rend.scene.append(Sphere(position=[0, -2, -5], radius=1, material = clear_glass))
rend.scene.append(Sphere(position=[3, -2, -5], radius=1, material = green_glass))


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
    
# pygame.image.save(screen, "output.bmp")


GenerateBMP('output.bmp', width, height, 3, rend.frameBuffer)

pygame.quit()