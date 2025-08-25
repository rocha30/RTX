import pygame 
from pygame.locals import *
from gl import * 
from figures import *
from BMP_Writer import GenerateBMP


width = 255
height = 255


screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.scene.append((Sphere((0, 0, -5), 0.5)))
rend.scene.append((Sphere((0, 0, -7), 0.1)))




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
