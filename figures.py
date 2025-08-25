import numpy as np 

class Shapes(object):
    def __init__(self, position):
        self.position = position
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return False


import numpy as np

class Sphere(Shapes):
    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius
        self.type = "Sphere"
    
    def solve_quadratic(self, a, b, c):
        """
        Resuelve ecuación cuadrática de manera numéricamente estable
        Retorna (tiene_solucion, t0, t1)
        """
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False, 0, 0
        elif discriminant == 0:
            t = -0.5 * b / a
            return True, t, t
        else:
            # Método numéricamente estable para evitar cancelación catastrófica
            if b > 0:
                q = -0.5 * (b + np.sqrt(discriminant))
            else:
                q = -0.5 * (b - np.sqrt(discriminant))
            
            t0 = q / a
            t1 = c / q
            
            # Asegurar que t0 <= t1
            if t0 > t1:
                t0, t1 = t1, t0
                
            return True, t0, t1
    
    def ray_intersect(self, orig, dir):
        """
        Versión simple: solo retorna True/False
        """
        # Vector del origen del rayo al centro de la esfera
        L = orig - self.position
        
        # Coeficientes de la ecuación cuadrática
        a = np.dot(dir, dir)
        b = 2.0 * np.dot(dir, L)
        c = np.dot(L, L) - self.radius * self.radius
        
        # Resolver ecuación cuadrática
        has_solution, t0, t1 = self.solve_quadratic(a, b, c)
        
        if not has_solution:
            return False
        
        # Si t0 es negativo, intentar con t1
        if t0 < 0:
            t0 = t1
            if t0 < 0:  # Ambos son negativos
                return False
        
        return True
    
    def ray_intersect_detailed(self, orig, dir):
        """
        Versión completa: retorna información detallada de la intersección
        """
        # Vector del origen del rayo al centro de la esfera
        L = orig - self.position
        
        # Coeficientes de la ecuación cuadrática
        a = np.dot(dir, dir)
        b = 2.0 * np.dot(dir, L)
        c = np.dot(L, L) - self.radius * self.radius
        
        # Resolver ecuación cuadrática
        has_solution, t0, t1 = self.solve_quadratic(a, b, c)
        
        if not has_solution:
            return None
        
        # Elegir la intersección más cercana que esté delante del rayo
        t = t0
        if t < 0:
            t = t1
            if t < 0:  # Ambos son negativos
                return None
        
        # Calcular punto de intersección y normal
        point = orig + t * dir
        normal = (point - self.position) / self.radius
        
        return {
            'distance': t,
            'point': point,
            'normal': normal,
            'object': self
        }

# Ejemplo de uso alternativo más simple (si no quieres cambiar mucho tu código actual)
class SphereSimple(Shapes):
    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius
        self.type = "Sphere"
    
    def ray_intersect(self, orig, dir):
        
        oc = orig - self.position
        a = np.dot(dir, dir)
        b = 2.0 * np.dot(oc, dir)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return False

        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        
        # Mejor lógica: usar la intersección más cercana que esté delante
        if t1 > 0 and t2 > 0:
            return True  # Al menos una intersección está delante
        elif t1 > 0 or t2 > 0:
            return True  # Una está delante
        else:
            return False  # Ambas están detrás