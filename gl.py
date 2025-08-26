from Camera import Camera
import numpy as np 
from math import *
import random
import pygame
from Material import *


class Renderer ():
    def __init__(self, screen, light_pos, light_intensity):
        self.scene = []
        self.screen = screen 
        _,_, self.width, self.height = screen.get_rect()

        self.camera = Camera ()
        self.glViewport( 0, 0, self.width, self.height)
        self.glProjection()
        self.glColor(1,1,1)
        
        self.glClearColor(0,0,0)

        self.glClear()


        self.light_pos = light_pos
        self.light_intensity = light_intensity

    def glViewport(self, x, y, width, height):
        self.vpX = round(x)
        self.vpY = round(y)
        self.vpWidth = width
        self.vpHeight = height

        self.viewportMatrix = np.matrix([[width/2, 0, 0 , x+width/2],
                                           [0, height/2, 0, y+height/2],
                                           [0,0,0.5,0.5],
                                           [0, 0, 1, 0]])

    def glProjection(self, n=0.1, f=1000, fov=60):
        aspectRatio = self.vpWidth / self.vpHeight
        fov *= pi / 180
        self.topEdge = tan(fov/2)*n
        self.RightEdge = self.topEdge * aspectRatio
        self.nearPlane = n
        self.projectionMatrix = np.matrix([[n/self.topEdge, 0,0,0],
                                           [0, n/self.RightEdge,0, 0],
                                           [0,0, -(f+n)/(f-n), -(2*f*n)/ (f-n)],
                                           [0,0,-1,0]])
        
    def glClearColor(self, r,g,b):

        r = min(1, max(0,r))
        g = min(1, max(0,g))
        b = min(1, max(0,b))

        self.clearColor = [r,g,b]
    
    def glColor (self, r,g,b):
        r = min(1, max(0,r))
        g = min(1, max(0,g))
        b = min(1, max(0,b))

        self.currColor = [r,g,b]
        
    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[color for y in range(self.height)]
                            for x in range(self.width)]

    def glPoint(self, x, y, color = None):
        # Dibuja un punto en la posición (x, y)
        x = round(x)
        y = round(y)

        if (0 <= x < self.width) and (0 <= y < self.height):
            color = [int (i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height -1 -y), color)
            self.frameBuffer[x][y] = color
            
    
    def glLine(self, p0, p1, color = None):

        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1] 
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return 
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        steep = dy > dx 
        if steep: 
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0 
        limit = 0.75
        m = dy / dx
        y = y0
        
        for i in range (round(x0), round(x1) + 1):
            if steep:
                self.glPoint(y,x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)
            
            if offset >= limit:
                if y0 < y1:
                    y+= 1
                else: 
                    y-= 1 
                limit 

    
        
    def glRender(self):
        indices = [(i,j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indices)
        
        for i,j in indices:
            x = i+self.vpX
            y = j+self.vpY
            if 0 <= x < self.vpWidth and 0 <= y < self.vpHeight:
                pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1
                pX *= self.RightEdge
                pY *= self.topEdge
                pZ = - self.nearPlane
                
                dir = np.array([pX, pY, pZ])
                dir = dir / np.linalg.norm(dir)

                hit = self.glCastRay(self.camera.translation, dir)
                if hit is not None:
                    self.glPoint(x, y)
                    pygame.display.flip()

    def glCastRay (self, origin, direction):
        closest_t = float('inf')
        hit_obj = None
        
        for obj in self.scene:
            t = obj.ray_intersect(origin, direction)
            if t and t < closest_t:
                closest_t = t
                hit_obj = obj

        if hit_obj:
            # Calcular la iluminación Phong en el punto de intersección
            P = origin + direction * closest_t
            N = hit_obj.get_normal(P)
            V = -direction/np.linalg.norm(-direction)

            color = hit_obj.material.phong_lighting(P, N, V, self.light_pos, self.light_intensity, hit_obj.material)

            return np.clip(color, 0, 1)
        else:
            return np.array([0, 0, 0])
