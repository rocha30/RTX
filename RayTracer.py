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

# Cámara en mejor posición para composición estética
rend.camera.set_position(0, 0.5, -6)

# Environment Map para reflejos de montañas
rend.envMap = BMPTexture('Fondo.bmp')

# ===== ESCENA PASO A PASO - EMPEZANDO SIMPLE =====

# === FONDO ZEN - SOLO ARENA Y ESFERAS ===

# Plano de arena (suelo) - más alejado para que se vea el horizonte
# Arena zen en el suelo (texturizada)
rend.scene.append(Plane(position=[0, -4, 0], normal=[0, 1, 0], material=sand_texture))

# 3 Esferas grandes oscuras (rocas zen) en el fondo - tamaños más proporcionados
rend.scene.append(Sphere(position=[-8, -3.5, -15], radius=1.0, material=rock_dark))
rend.scene.append(Sphere(position=[8, -3.5, -12], radius=0.8, material=rock_dark))
rend.scene.append(Sphere(position=[5, -3.8, -18], radius=1.2, material=rock_dark))

# === STAND/MESA DE MADERA ===
# Mesa rectangular de madera que sostiene la vitrina (proporcionada para la nueva escala)
rend.scene.append(AABB(min_point=[-1.5, -2.5, -6], max_point=[1.5, -2.2, -3], 
                      material=wood_dark))

# Pedestal/base sólida del stand (más elegante que patas individuales)
pedestal_width = 1.2
pedestal_depth = 2.5
pedestal_height = 2.0

rend.scene.append(AABB(min_point=[-pedestal_width/2, -4.5, -pedestal_depth/2-4.5], 
                      max_point=[pedestal_width/2, -4.5+pedestal_height, pedestal_depth/2-4.5], 
                      material=wood_dark))

# === PEDESTAL GRANDE PARA TODAS LAS FIGURAS ===
# Hacemos un pedestal más grande para acomodar todas las figuras sin vitrina
pedestal_size = 4.0  # Mucho más grande para todas las figuras
pedestal_height = 0.3  # Altura del pedestal

# Base grande del pedestal de madera con textura
rend.scene.append(AABB(min_point=[-pedestal_size/2, -2.5, -pedestal_size/2-4.5], 
                      max_point=[pedestal_size/2, -2.2, pedestal_size/2-4.5], 
                      material=wood_textured))

# === TODAS LAS FIGURAS EN EL PEDESTAL - COMPOSICIÓN MEJORADA ===

# Esferas de diferentes materiales (disposición más orgánica)
rend.scene.append(Sphere(position=[-1.2, -1.8, -4.8], radius=0.25, material=wood_light))  # Madera clara
rend.scene.append(Sphere(position=[0.9, -1.6, -4.2], radius=0.22, material=mirror))       # Espejo
rend.scene.append(Sphere(position=[-0.4, -2.0, -3.8], radius=0.2, material=metal))       # Metal

# Esfera roja opaca
rend.scene.append(Sphere(position=[1.3, -1.9, -4.6], radius=0.18, material=red_plastic))

# Esfera emisiva (que da luz suave naranja) - más centrada
rend.scene.append(Sphere(position=[0.1, -1.4, -4.2], radius=0.15, material=emissive_orange))

# Cilindros de diferentes materiales (mejor espaciados)
rend.scene.append(Cylinder(position=[-1.6, -1.8, -3.6], axis=[0, 1, 0], radius=0.15, height=0.4, material=polished_gold))
rend.scene.append(Cylinder(position=[1.4, -1.7, -5.1], axis=[0, 1, 0], radius=0.12, height=0.35, material=brass_shiny))

# Cubos/AABBs como figuras geométricas (mejor posicionados)
rend.scene.append(AABB(min_point=[-0.9, -2.1, -5.3], max_point=[-0.6, -1.8, -5.0], material=glossy_blue))
rend.scene.append(AABB(min_point=[0.3, -2.0, -3.7], max_point=[0.6, -1.7, -3.4], material=lacquer_red))

# === FIGURAS GEOMÉTRICAS NUEVAS - COMPOSICIÓN MEJORADA (20 PUNTOS) ===

# 1. Torus (Dona) - posición más visible
rend.scene.append(Torus(position=[-0.6, -1.5, -4.1], major_radius=0.25, minor_radius=0.08, material=polished_silver))

# 2. Cone (Cono) - mejor proporción
rend.scene.append(Cone(tip=[0.7, -1.3, -4.9], base_center=[0.7, -2.0, -4.9], radius=0.18, material=matte_red))

# 3. Pyramid (Pirámide) - más centrada
pyramid_base = [
    [-0.05, -2.1, -4.6],  # vértice 1 de la base
    [0.25, -2.1, -4.6],   # vértice 2 de la base  
    [0.1, -2.1, -4.2]     # vértice 3 de la base
]
rend.scene.append(Pyramid(apex=[0.1, -1.6, -4.4], base_vertices=pyramid_base, material=soft_gold))

# 4. Ellipsoid (Elipsoide) - mejor posición
rend.scene.append(Ellipsoid(position=[1.1, -1.8, -3.9], semi_axes=[0.12, 0.22, 0.08], material=pale_blue))

# === ILUMINACIÓN MÚLTIPLE MEJORADA (10 PUNTOS) ===

# 1. Luz ambiental suave
rend.lights.append(AmbientLight(intensity=0.2))

# 2. Luz direccional principal del atardecer (más suave)
rend.lights.append(DirectionalLight(
    color=[1.0, 0.8, 0.6],
    direction=[0.3, -0.7, -0.5],
    intensity=0.5
))

# 3. Luz direccional secundaria (luz de relleno azulada)
rend.lights.append(DirectionalLight(
    color=[0.6, 0.7, 1.0],
    direction=[-0.2, -0.5, 0.3],
    intensity=0.2
))

# 4. Point Light alejada del pedestal (iluminación más suave)
rend.lights.append(PointLight(
    color=[1.0, 0.9, 0.7],
    position=[0, 1, -2],      # Más arriba y más lejos
    intensity=0.8             # Menos intensidad
))

# 5. Point Light azul para ambiente (más alejada)
rend.lights.append(PointLight(
    color=[0.7, 0.8, 1.0],
    position=[-3, 1, -2],     # Más alejada
    intensity=0.6             # Menos intensidad
))

# 6. Spot Light enfocando el centro del pedestal (más suave)
rend.lights.append(SpotLight(
    color=[1.0, 1.0, 0.9],
    position=[0, 3, -1],      # Más arriba
    direction=[0, -1, -1],
    intensity=1.2,            # Menos intensidad
    innerAngle=25,
    outerAngle=40
))

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

# Generar imagen final
GenerateBMP('output.bmp', width, height, 3, rend.frameBuffer)

pygame.quit()