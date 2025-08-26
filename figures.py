import numpy as np 

class Shapes(object):
    def __init__(self, position):
        self.position = position
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return False


class Sphere(Shapes):
    def __init__(self, position, radius, material):
        super().__init__(position)
        self.radius = radius
        self.type = "Sphere"
        self.material = material

    def get_normal(self, point):
        return (point - self.position) / np.linalg.norm(point - self.position)

    def ray_intersect(self, orig, dir):
        oc = orig - self.position
        a = np.dot(dir, dir)
        b = 2.0 * np.dot(oc, dir)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None  # No hay intersección
        
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        
        
        if t1 > 0 and t2 > 0:
            return min(t1, t2)  # La más cercana
        elif t1 > 0:
            return t1
        elif t2 > 0:
            return t2
        else:
            return None  # Ambas están detrás