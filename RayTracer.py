import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from figures import *
from lights import *
from Material import *

width = 720
height = 720

pygame.init()  # Inicializar pygame
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption("Ray Tracer")  # Título de la ventana
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.camera.translation = [0, 0, -1]

#Spheres 
rend.scene.append(Sphere(position=[1, -1, -5], radius=1.0, material = red_material))
rend.scene.append(Sphere(position=[0, 0, -7], radius=0.5, material = red_material))


# Luces
rend.lights.append(AmbientLight())
rend.lights.append(DirectionalLight(direction=[-1, -1, -1]))


rend.glRender()


pygame.display.flip()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
    
    # Mover clock.tick dentro del loop
    clock.tick(60)


GenerateBMP('output.bmp', width, height, 3, rend.frameBuffer)

pygame.quit()