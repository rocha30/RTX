from numpy import *
import numpy as np 
from intercept import *
from MathLib import *
from Material import *

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
        self.normal = normal / np.linalg.norm(normal)
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        if isclose (0, denom):
            return None  # El rayo es paralelo al plano
        d = np.dot(np.subtract(self.position, orig), self.normal) 
        
        t = d / denom
        if t < 0:
            return None  
        
        P = np.add(orig, np.multiply(dir, t))
            
        
        return Intercept(point = P, 
                         normal = self.normal, 
                         distance = t, 
                         rayDirection = dir, 
                         obj = self, 
                         texCoords = None)
    
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
        
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        # Usar la intersección del plano padre
        plane_hit = super().ray_intersect(orig, dir)
        
        if plane_hit is None:
            return None
        
        # Verificar que el punto está dentro del radio
        if np.linalg.norm(plane_hit.point - self.position) <= self.radius:
            # Cambiar el tipo de objeto en el intercept para que sea el disco
            return Intercept(
                point=plane_hit.point,
                normal=plane_hit.normal,
                distance=plane_hit.distance,
                rayDirection=plane_hit.rayDirection,
                obj=self,  #self del disco, no del plano 
                texCoords=plane_hit.texCoords
            )
        
        return None


class OBB(Shapes):

    def __init__(self, center, axes, extents, material):
        super().__init__(position=np.array(center, dtype=float), material=material)
        # Ensure axes are numpy arrays and orthonormalize defensively
        a0 = np.array(axes[0], dtype=float)
        a1 = np.array(axes[1], dtype=float)
        a2 = np.array(axes[2], dtype=float)

        # Orthonormalize via Gram-Schmidt (in case input isn't perfect)
        def norm(v):
            n = np.linalg.norm(v)
            return v / n if n != 0 else v

        u0 = norm(a0)
        u1 = a1 - np.dot(a1, u0) * u0
        u1 = norm(u1)
        u2 = a2 - np.dot(a2, u0) * u0 - np.dot(a2, u1) * u1
        u2 = norm(u2)

        self.axes = np.stack([u0, u1, u2], axis=0)  # 3x3 matrix (rows are axes)
        self.extents = np.array(extents, dtype=float)
        self.type = "OBB"

    def ray_intersect(self, orig, dir):
        """Transform the ray into the OBB local space (where the box is axis-aligned)
        and perform a slab/AABB intersection test. Returns an Intercept or None.
        """
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)

        # Build rotation matrix from world to OBB local: columns are axes, so use transpose
        R = self.axes.T  # world->local rotation (3x3)

        # Translate origin to OBB local center and rotate
        local_orig = np.dot(R, (orig - self.position))
        local_dir = np.dot(R, dir)

        # Now we have an AABB from -extents to +extents in local space
        epsilon = 1e-8
        tmin = -np.inf
        tmax = np.inf

        for i in range(3):
            if abs(local_dir[i]) < epsilon:
                # Ray parallel to slab; if origin not within slab -> no hit
                if local_orig[i] < -self.extents[i] or local_orig[i] > self.extents[i]:
                    return None
                # Otherwise, it passes this slab - continue
            else:
                t1 = (-self.extents[i] - local_orig[i]) / local_dir[i]
                t2 = ( self.extents[i] - local_orig[i]) / local_dir[i]
                t_near_i = min(t1, t2)
                t_far_i = max(t1, t2)
                tmin = max(tmin, t_near_i)
                tmax = min(tmax, t_far_i)
                if tmin > tmax:
                    return None

        if tmax < 0:
            return None

        t_local = tmin if tmin >= 0 else tmax
        # Intersection point in local space
        P_local = local_orig + local_dir * t_local

        # Compute intersection point back in world space
        P_world = np.dot(self.axes.T.T, P_local) + self.position  # axes.T.T == axes

        # Compute normal: determine which face was hit by checking which component is near extent
        normal_local = np.zeros(3, dtype=float)
        eps_norm = 1e-6
        for i in range(3):
            if abs(P_local[i] - self.extents[i]) < eps_norm:
                normal_local[i] = 1.0
                break
            if abs(P_local[i] + self.extents[i]) < eps_norm:
                normal_local[i] = -1.0
                break

        # Transform normal back to world space (rotate by axes matrix)
        normal_world = np.dot(self.axes.T.T, normal_local)
        nrm = np.linalg.norm(normal_world)
        if nrm != 0:
            normal_world /= nrm
        else:
            normal_world = np.array([0.0, 1.0, 0.0])

        return Intercept(
            point=P_world,
            normal=normal_world,
            distance=t_local,
            rayDirection=dir,
            obj=self,
            texCoords=None
        )




class TruncatedSphere(Shapes):
    """Truncated Sphere - a sphere cut by two parallel planes.
    
    Constructor: TruncatedSphere(position, radius, y_min, y_max, material)
    - position: center of the original sphere
    - radius: radius of the sphere
    - y_min, y_max: Y-coordinate limits for truncation (in world coordinates)
    """
    def __init__(self, position, radius, y_min, y_max, material):
        super().__init__(position, material)
        self.radius = float(radius)
        self.y_min = float(y_min)
        self.y_max = float(y_max)
        self.type = "TruncatedSphere"
        
    def ray_intersect(self, orig, dir):
        """Ray-Truncated Sphere intersection.
        First find sphere intersection, then check Y bounds."""
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        # Standard sphere intersection
        L = self.position - orig
        tca = np.dot(L, dir)
        d_squared = np.dot(L, L) - tca * tca
        
        if d_squared > self.radius * self.radius:
            return None
        
        thc = np.sqrt(self.radius * self.radius - d_squared)
        
        t0 = tca - thc
        t1 = tca + thc
        
        # Try both intersection points
        candidates = []
        if t0 > 1e-6:
            candidates.append(t0)
        if t1 > 1e-6 and t1 != t0:
            candidates.append(t1)
            
        if not candidates:
            return None
            
        # Check which intersection points fall within Y bounds
        for t in sorted(candidates):
            P = orig + t * dir
            
            # Check if intersection point is within truncation bounds
            if self.y_min <= P[1] <= self.y_max:
                # Calculate normal (same as regular sphere)
                normal = P - self.position
                norm_length = np.linalg.norm(normal)
                
                if norm_length > 1e-8:
                    normal = normal / norm_length
                else:
                    normal = np.array([0.0, 1.0, 0.0])  # fallback
                
                # Calculate spherical UV coordinates
                u = np.arctan2(normal[2], normal[0]) / (2 * np.pi) + 0.5
                v = np.arccos(-normal[1]) / np.pi
                
                return Intercept(
                    point=P,
                    normal=normal,
                    distance=t,
                    rayDirection=dir,
                    obj=self,
                    texCoords=[u, v]
                )
        
        return None  # No valid intersection within bounds

    

    