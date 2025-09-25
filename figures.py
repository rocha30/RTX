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
        norm = np.linalg.norm(normal)
        if norm != 0:
            normal /= norm
        else:
            normal = np.array([0, 1, 0])  # default normal if point is at center
        
        
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

class Plane(Shapes):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        norm = np.linalg.norm(normal)
        if norm != 0:
            self.normal = normal / norm
        else:
            self.normal = np.array([0, 0, 1])  # default normal
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        if abs(denom) > 1e-6:
            d = np.dot(np.subtract(self.position, orig), self.normal) / denom
            if d >= 0:
                P = np.add(orig, np.multiply(dir, d))
                return Intercept(
                    point=P,
                    normal=self.normal,
                    distance=d,
                    rayDirection=dir,
                    obj=self,
                    texCoords=None  
                )
        return None
    
class Triangle(Shapes):
    def __init__(self, v0, v1, v2, material):
        super().__init__(position=None, material=material)
        self.v0 = np.array(v0, dtype=float)
        self.v1 = np.array(v1, dtype=float)
        self.v2 = np.array(v2, dtype=float)
        self.type = "Triangle"
        self.normal = np.cross(self.v1 - self.v0, self.v2 - self.v0)
        
        norm = np.linalg.norm(self.normal)
        if norm != 0:
            self.normal = self.normal / norm
        else: 
            self.normal = np.array([0, 0, 1], dtype=float)

    def ray_intersect(self, orig, dir):
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        h = np.cross(dir, edge2)
        a = np.dot(edge1, h)
        
        if abs(a) < 1e-6:
            return None
        
        f = 1.0 / a
        s = orig - self.v0
        u = f * np.dot(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        q = np.cross(s, edge1)
        v = f * np.dot(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None
        
        t = f * np.dot(edge2, q)
        
        if t > 1e-6:
            P = orig + dir * t
            return Intercept(
                point=P,
                normal=self.normal,
                distance=t,
                rayDirection=dir,
                obj=self,
                texCoords=None  
            )
        
        return None

class AABB(Shapes):
    def __init__(self, min_point, max_point, material):
        super().__init__(position=None, material=material)
        self.min_point = np.array(min_point, dtype=float)
        self.max_point = np.array(max_point, dtype=float)
        self.type = "AABB"

    def ray_intersect(self, orig, dir):
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        # Evitar división por cero
        epsilon = 1e-8
        tmin = np.full(3, float('-inf'), dtype=float)
        tmax = np.full(3, float('inf'), dtype=float)
        
        for i in range(3):
            if abs(dir[i]) < epsilon:
                # Rayo paralelo a este plano
                if orig[i] < self.min_point[i] or orig[i] > self.max_point[i]:
                    return None  # No intersecta
                # Para planos paralelos, mantenemos los valores por defecto
            else:
                t1 = (self.min_point[i] - orig[i]) / dir[i]
                t2 = (self.max_point[i] - orig[i]) / dir[i]
                tmin[i] = np.minimum(t1, t2)
                tmax[i] = np.maximum(t1, t2)
        
        t_near = np.max(tmin)
        t_far = np.min(tmax)
        
        if t_near > t_far or t_far < 0:
            return None
        
        t = t_near if t_near >= 0 else t_far
        P = orig + dir * t
        
        # Calcular la normal del punto de intersección
        epsilon = 1e-6
        normal = np.zeros(3, dtype=float)
        
        for i in range(3):
            if abs(P[i] - self.min_point[i]) < epsilon:
                normal[i] = -1
                break
            elif abs(P[i] - self.max_point[i]) < epsilon:
                normal[i] = 1
                break
        
        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            rayDirection=dir,
            obj=self,
            texCoords=None  
        )
        
class Disk (Shapes):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, material)
        norm = np.linalg.norm(normal)
        if norm != 0:
            self.normal = normal / norm
        else:
            self.normal = np.array([0, 1, 0])  # default normal (up)
        self.radius = radius
        self.type = "Disk"

    
    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        if abs(denom) > 1e-6:
            d = np.dot(np.subtract(self.position, orig), self.normal) / denom
            if d >= 0:  # La intersección debe estar hacia adelante
                P = np.add(orig, np.multiply(dir, d))  # Punto de intersección
                if np.linalg.norm(P - self.position) <= self.radius:  # Verificar que el punto está dentro del radio
                    return Intercept(
                        point=P,
                        normal=self.normal,
                        distance=d,
                        rayDirection=dir,
                        obj=self,
                        texCoords=None  
                    )
        return None

    

    