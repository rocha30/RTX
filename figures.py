from numpy import *
import numpy as np 
from intercept import *

class Shapes(object):
    def __init__(self, position, material):
        self.position = position
        self.type = "None"
        self.material = material

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shapes):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def get_normal(self, point):
        return (point - self.position) / np.linalg.norm(point - self.position)

    def ray_intersect(self, orig, dir):
        L = np.subtract(self.position, orig)
        tca = np.dot(L, dir)
        d = (np.linalg.norm(L)**2 - tca**2)**0.5
        
        if d > self.radius:
            return None
        
        thc = (self.radius**2 - d**2)**0.5
        
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = np.add(orig, np.multiply(dir, t0))
        
        normal = np.subtract(P, self.position)
        normal /= np.linalg.norm(normal)
        
        
        # Obtener las coordenadas de textura
        u = atan2(normal[2], normal[0]) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi 

        # Retornar el objeto Intercept con toda la información
        return Intercept(
            point=P, 
            normal=normal, 
            distance=t0, 
            rayDirection=dir, 
            obj=self, 
            texCoords=[u,v]  
        )
