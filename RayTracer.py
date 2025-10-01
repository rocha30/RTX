import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from BMPTexture import BMPTexture
from figures import *
from lights import *
from Material import *

width = 800
height = 600

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)


# rend.envMap = BMPTexture('Fondo.bmp')



# CUARTO: 5 PLANOS con colores más contrastantes
# Piso (más claro)
rend.scene.append(Plane(position=[0, -3, 0], normal=[0, 1, 0], 
                       material=Material(diffuse=[0.8, 0.8, 0.8], spec=16, ks=0.0, matType=OPAQUE)))
# Techo (blanco brillante)
rend.scene.append(Plane(position=[0, 3, 0], normal=[0, -1, 0], 
                       material=Material(diffuse=[0.95, 0.95, 0.95], spec=8, ks=0.0, matType=OPAQUE)))
# Pared trasera (beige claro)
rend.scene.append(Plane(position=[0, 0, -10], normal=[0, 0, 1], 
                       material=Material(diffuse=[0.9, 0.85, 0.75], spec=8, ks=0.0, matType=OPAQUE)))
# Pared izquierda (crema)
rend.scene.append(Plane(position=[-4, 0, 0], normal=[1, 0, 0], 
                       material=Material(diffuse=[0.85, 0.8, 0.7], spec=8, ks=0.0, matType=OPAQUE)))
# Pared derecha (azul muy claro)
rend.scene.append(Plane(position=[4, 0, 0], normal=[-1, 0, 0], 
                       material=Material(diffuse=[0.85, 0.9, 0.95], spec=8, ks=0.0, matType=OPAQUE)))



# LAB 8: Cylinder y Torus - 3 instancias de cada uno con materiales diferentes

# LAB 8: Cylinder y Torus - 3 instancias de cada uno con materiales diferentes

# === 3 Cylinders con diferentes materiales (lado izquierdo) ===
# Cylinder 1: Opaco rojo (pequeño vertical, izquierda abajo)
rend.scene.append(Cylinder(position=[-2.5, -1, -5], 
                          axis=[0, 1, 0], 
                          radius=0.4, 
                          height=1.2, 
                          material=Material(diffuse=[0.9, 0.2, 0.2], spec=32, ks=0.0, matType=OPAQUE)))

# Cylinder 2: Reflectivo dorado (mediano diagonal, izquierda centro)
rend.scene.append(Cylinder(position=[-2, 0.5, -7], 
                          axis=[0.3, 1, 0.2],  # Ligeramente inclinado
                          radius=0.5, 
                          height=1.5, 
                          material=Material(diffuse=[0.8, 0.6, 0.1], spec=64, ks=0.8, matType=REFLECTIVE)))

# Cylinder 3: Transparente azul (grande horizontal, izquierda arriba)
rend.scene.append(Cylinder(position=[-1.5, 1.8, -6], 
                          axis=[1, 0.2, 0],  # Casi horizontal
                          radius=0.3, 
                          height=2.0, 
                          material=Material(diffuse=[0.8, 0.9, 1.0], spec=128, ks=0.0, ior=1.5, matType=TRANSPARENT)))

# === 3 Torus con diferentes materiales (lado derecho) ===
# Torus 1: Opaco azul brillante (pequeño, derecha abajo)
rend.scene.append(Torus(position=[2, -1.8, -4.5], 
                       major_radius=0.6, 
                       minor_radius=0.25, 
                       material=Material(diffuse=[0.2, 0.3, 0.9], spec=32, ks=0.0, matType=OPAQUE)))

# Torus 2: Reflectivo rojo (mediano, derecha centro)
rend.scene.append(Torus(position=[2.5, 0, -6], 
                       major_radius=0.8, 
                       minor_radius=0.3, 
                       material=Material(diffuse=[0.8, 0.1, 0.1], spec=96, ks=0.7, matType=REFLECTIVE)))

# Torus 3: Reflectivo metálico (grande, derecha arriba) - CAMBIADO DE TRANSPARENTE
rend.scene.append(Torus(position=[1.8, 1.5, -7.5], 
                       major_radius=1.0, 
                       minor_radius=0.4, 
                       material=Material(diffuse=[0.7, 0.7, 0.9], spec=128, ks=0.85, matType=REFLECTIVE)))
 

# Luces mejoradas para mejor visibilidad
rend.lights.append(AmbientLight(intensity=0.6))  # Más luz ambiental
rend.lights.append(DirectionalLight(direction=[0, -1, -1], intensity=0.8))
rend.lights.append(PointLight(position=[-2, 2, -3], intensity=0.7))  # Luz desde arriba-izquierda  
rend.lights.append(PointLight(position=[2, 1, -4], intensity=0.6))   # Luz desde derecha
rend.lights.append(PointLight(position=[0, -1, -2], intensity=0.5))  # Luz frontal baja




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