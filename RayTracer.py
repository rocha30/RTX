import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from BMPTexture import BMPTexture
from figures import *
from lights import *
from Material import *

width = 256
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)


# rend.envMap = BMPTexture('Fondo.bmp')



# CUARTO: 5 PLANOS (mantener para contexto visual)
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

# TORUS - 3 instancias con diferentes tamaños, posiciones y materiales
# Torus 1: Pequeño, opaco (rojo mate)
# rend.scene.append(Torus(position=[-2, 0, -6], major_radius=0.8, minor_radius=0.3, material=matte_red))
# # Torus 2: Mediano, reflectivo (dorado pulido)
# rend.scene.append(Torus(position=[0, 0, -7], major_radius=1.0, minor_radius=0.4, material=polished_gold))
# # Torus 3: Grande, transparente (vidrio claro)
# rend.scene.append(Torus(position=[2, 1, -8], major_radius=1.2, minor_radius=0.5, material=matte_red))

# TRUNCATED SPHERE - 3 instancias con diferentes tamaños, posiciones y materiales
# TruncatedSphere 1: Pequeña, opaca (azul brillante)
rend.scene.append(TruncatedSphere(position=[-1.5, -1, -5], radius=0.7, y_min=-1.5, y_max=-0.3, material=glossy_blue))
# TruncatedSphere 2: Mediana, reflectiva (rojo lacado)
# rend.scene.append(TruncatedSphere(position=[1.5, 0, -6], radius=0.9, y_min=-0.4, y_max=0.8, material=lacquer_red))
# # TruncatedSphere 3: Grande, transparente (vidrio verde)
# rend.scene.append(TruncatedSphere(position=[0, -1.5, -7.5], radius=1.1, y_min=-2.3, y_max=-0.7, material=green_glass))



 

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