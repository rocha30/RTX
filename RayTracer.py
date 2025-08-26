import pygame 
from pygame.locals import *
from gl import * 
from figures import *
from BMP_Writer import GenerateBMP


width = 256
height = 256


screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

light_pos = np.array((0, 5, -5))
light_intensity = 1.0

rend = Renderer(screen, light_pos, light_intensity)

red_material = Material(ka=0.1, kd=0.6, ks=0.3, shininess=50, color=(1, 0, 0))
blue_material = Material(ka=0.1, kd=0.6, ks=0.3, shininess=50, color=(0, 0, 1))

rend.scene.append(Sphere((1, 0, -2), radius=0.5, material=red_material))
rend.scene.append(Sphere((-1, 0, -3), radius=0.7, material=blue_material))

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                isRunning = False



    rend.glRender()
    pygame.display.flip()

    clock.tick(60)


GenerateBMP('output.bmp', width, height, 3, rend.frameBuffer)

pygame.quit()


