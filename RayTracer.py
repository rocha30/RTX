import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from BMPTexture import BMPTexture
from figures import *
from lights import *
from Material import *

width = 512
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)


# rend.envMap = BMPTexture('Fondo.bmp')



# CUARTO: 5 PLANOS con colores más suaves
# Piso
rend.scene.append(Plane(position=[0, -3, 0], normal=[0, 1, 0], material=warm_gray))
# Techo  
rend.scene.append(Plane(position=[0, 3, 0], normal=[0, -1, 0], material=soft_white))
# Pared trasera
rend.scene.append(Plane(position=[0, 0, -10], normal=[0, 0, 1], material=light_beige))
# Pared izquierda
rend.scene.append(Plane(position=[-4, 0, 0], normal=[1, 0, 0], material=light_beige))
# Pared derecha  
rend.scene.append(Plane(position=[4, 0, 0], normal=[-1, 0, 0], material=pale_blue))

# DOS CUBOS (usando AABB) - CORREGIDOS
# Cubo 1: pequeño (1x1x1) flotando a la izquierda
rend.scene.append(AABB(min_point=[-2.5, -2, -7], max_point=[-1.5, -1, -6], material=matte_red))
# Cubo 2: más grande (1.5x1.5x1.5) flotando a la derecha
rend.scene.append(AABB(min_point=[1, -2.5, -7.5], max_point=[2.5, -1, -6], material=glossy_blue))

# UN TRIÁNGULO (vertical, como una pared triangular)
rend.scene.append(Triangle(v0=[0, -1, -6], v1=[-1, 1, -5], v2=[1, 1, -5], material=green_glass))

# UN DISCO vertical en la pared (como un escudo o medallón)
rend.scene.append(Disk(position=[-3.5, 0, -7], normal=[1, 0, 0], radius=0.8, material=soft_gold))



 

# Luces mejoradas para mejor iluminación
rend.lights.append(AmbientLight(intensity=0.4))  # más luz ambiental
rend.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity = 0.6))
rend.lights.append(PointLight(position=[0, 2, -4], intensity=0.8))  # luz desde arriba
rend.lights.append(PointLight(position=[-2, 1, -5], intensity=0.4))  # luz lateral suave



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