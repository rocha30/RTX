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
        # Convertir a arrays de numpy para asegurar compatibilidad
        orig = np.array(orig)
        dir = np.array(dir)
        
        # Calcular la intersección rayo-esfera
        oc = orig - self.position
        a = np.dot(dir, dir)
        b = 2.0 * np.dot(oc, dir)
        c = np.dot(oc, oc) - self.radius * self.radius
        
        discriminant = b * b - 4 * a * c
        
        # Si no hay intersección, retornar None
        if discriminant < 0:
            return None
        
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        
        # Seleccionar el valor t apropiado (la intersección más cercana y positiva)
        t = None
        if t1 > 0 and t2 > 0:
            t = min(t1, t2)
        elif t1 > 0:
            t = t1
        elif t2 > 0:
            t = t2
        else:
            return None  # Ambas intersecciones están detrás del origen del rayo
        
        # Calcular el punto de intersección
        point = orig + dir * t
        
        # Calcular la normal en el punto de intersección
        n = point - self.position
        normal = n / np.linalg.norm(n)
        
        # Retornar el objeto Intercept con toda la información
        return Intercept(
            point=point, 
            normal=normal, 
            distance=t, 
            rayDirection=dir, 
            obj=self
        )
