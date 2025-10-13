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

# Environment Map para reflejos y refracciones
# rend.envMap = BMPTexture('Fondo.bmp')

# ===== ESCENA COMPLEJA LAB FINAL - VITRINA DE CRISTAL =====

# === FONDO ZEN ===

# Plano de arena con textura de ondas
rend.scene.append(Plane(position=[0, -4, 0], normal=[0, 1, 0], 
                       material=sand_texture))

# 3 Esferas grandes oscuras (rocas zen)
rend.scene.append(Sphere(position=[-8, -2.5, -15], radius=1.5, material=rock_dark))
rend.scene.append(Sphere(position=[8, -2, -12], radius=1.2, material=rock_dark))
rend.scene.append(Sphere(position=[6, -2.8, -18], radius=1.8, material=rock_dark))

# Estanque rectangular (cubo de agua)
rend.scene.append(AABB(min_point=[4, -3.8, -10], max_point=[7, -3.5, -7], 
                      material=water_material))

# === BASE DE MADERA ===
# Base para la vitrina
rend.scene.append(AABB(min_point=[-3, -3.8, -8], max_point=[3, -3.5, -2], 
                      material=wood_dark))

# === VITRINA TRANSPARENTE GRANDE ===
# Paredes de la vitrina (dejando espacio interior)
vitrina_thickness = 0.1

# Pared frontal
rend.scene.append(AABB(min_point=[-2.5, -3.5, -2], max_point=[2.5, 2, -2+vitrina_thickness], 
                      material=display_glass))
# Pared trasera
rend.scene.append(AABB(min_point=[-2.5, -3.5, -7], max_point=[2.5, 2, -7+vitrina_thickness], 
                      material=display_glass))
# Pared izquierda
rend.scene.append(AABB(min_point=[-2.5, -3.5, -7], max_point=[-2.5+vitrina_thickness, 2, -2], 
                      material=display_glass))
# Pared derecha
rend.scene.append(AABB(min_point=[2.5-vitrina_thickness, -3.5, -7], max_point=[2.5, 2, -2], 
                      material=display_glass))
# Techo de vitrina
rend.scene.append(AABB(min_point=[-2.5, 2-vitrina_thickness, -7], max_point=[2.5, 2, -2], 
                      material=display_glass))

# === CONTENIDO DE LA VITRINA (11+ figuras) ===

# 3 Esferas transparentes (cristal)
rend.scene.append(Sphere(position=[-1.5, -2, -4], radius=0.4, material=crystal_clear))
rend.scene.append(Sphere(position=[0, -1.5, -5.5], radius=0.3, material=crystal_clear))
rend.scene.append(Sphere(position=[1.2, -2.2, -3.5], radius=0.35, material=crystal_clear))

# 1 Cubo dorado (reflectante)
rend.scene.append(AABB(min_point=[-0.8, -3.2, -4.5], max_point=[-0.2, -2.6, -3.9], 
                      material=polished_gold))

# 1 Cilindro azul (brillante)
rend.scene.append(Cylinder(position=[1.5, -2.5, -5], 
                          axis=[0, 1, 0], 
                          radius=0.25, 
                          height=0.8, 
                          material=brass_shiny))

# 1 Pirámide verde (transparente/refractiva)
pyramid_base = [
    [-0.3, -3.4, -6.2],  # v0
    [0.3, -3.4, -6.2],   # v1
    [0, -3.4, -5.6]      # v2
]
rend.scene.append(Pyramid(apex=[0, -2.5, -5.9], base_vertices=pyramid_base, 
                         material=crystal_green))

# 1 Cubo negro (mate)
rend.scene.append(AABB(min_point=[0.8, -3.3, -6.5], max_point=[1.4, -2.7, -5.9], 
                      material=matte_black))

# 1 Toroide gris/morado
rend.scene.append(Torus(position=[-1, -1, -4.5], 
                       major_radius=0.4, 
                       minor_radius=0.15, 
                       material=torus_purple))

# 1 Cono pequeño
rend.scene.append(Cone(tip=[0.5, -1.8, -4.8], 
                      base_center=[0.5, -3.2, -4.8], 
                      radius=0.2, 
                      material=copper_aged))

# 1 Esfera emisiva naranja (que genera luz)
rend.scene.append(Sphere(position=[-0.8, -0.5, -5], radius=0.2, material=emissive_orange))

# 1 Esfera roja transparente/refractiva
rend.scene.append(Sphere(position=[1.8, -1.8, -6], radius=0.25, material=crystal_red))

# 1 Cilindro pequeño de madera (soporte)
rend.scene.append(Cylinder(position=[0, -3.3, -3.8], 
                          axis=[0, 1, 0], 
                          radius=0.1, 
                          height=0.3, 
                          material=wood_light))

# === ILUMINACIÓN COMPLEJA ===

# Luz ambiental suave
rend.lights.append(AmbientLight(intensity=0.3))

# Luz direccional del atardecer (cálida, desde un lado)
rend.lights.append(DirectionalLight(
    color=[1.0, 0.8, 0.6],       # luz cálida del atardecer
    direction=[0.3, -0.5, -0.7], # desde arriba y lateral
    intensity=0.8
))

# Luz puntual de la esfera emisiva (simulando que irradia luz)
rend.lights.append(PointLight(
    position=[-0.8, -0.5, -5],   # misma posición que esfera naranja
    color=[1.0, 0.6, 0.2],       # color naranja
    intensity=0.6
))

# Luz de relleno suave desde el frente
rend.lights.append(PointLight(
    position=[0, 2, 2],
    color=[0.9, 0.9, 1.0],       # luz fría de relleno
    intensity=0.4
))

# Luz lateral para crear contraste
rend.lights.append(PointLight(
    position=[4, 1, -4],
    color=[1.0, 0.9, 0.7],
    intensity=0.5
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