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
        # Numeric stability: clamp tiny negatives before sqrt
        d2 = np.linalg.norm(L)**2 - tca**2
        if d2 < 0:
            d2 = 0.0
        d = np.sqrt(d2)
        
        if d > self.radius:
            return None
        
        # Clamp again to avoid -0.0 under sqrt from rounding
        thc2 = self.radius**2 - d**2
        if thc2 < 0:
            thc2 = 0.0
        thc = np.sqrt(thc2)
        
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
    """Oriented Bounding Box defined by a center position, local axes (3 orthonormal vectors)
    and half-sizes (extents) along those axes.

    Constructor signature:
        OBB(center, axes, extents, material)

    - center: [x,y,z]
    - axes: list of 3 orthonormal vectors [[ax,ay,az], [bx,by,bz], [cx,cy,cz]]
    - extents: [ex,ey,ez] (positive half-sizes)
    """
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
        tmin = float('-inf')
        tmax = float('inf')

        for i in range(3):
            if abs(local_dir[i]) < epsilon:
                # Ray parallel to slab; if origin not within slab -> no hit
                if local_orig[i] < -self.extents[i] or local_orig[i] > self.extents[i]:
                    return None
                # Otherwise, it passes this slab - continue
            else:
                t1 = float((-self.extents[i] - local_orig[i]) / local_dir[i])
                t2 = float(( self.extents[i] - local_orig[i]) / local_dir[i])
                # Use explicit comparison to avoid numpy's min/max wrappers
                if t1 < t2:
                    t_near_i = t1
                    t_far_i = t2
                else:
                    t_near_i = t2
                    t_far_i = t1
                # Update tmin/tmax with explicit comparisons (avoid numpy wrappers)
                if t_near_i > tmin:
                    tmin = t_near_i
                if t_far_i < tmax:
                    tmax = t_far_i
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


class Torus(Shapes):
    """Torus (donut shape) defined by major radius R (center to tube center) 
    and minor radius r (tube radius). Centered at position with axis along Y.
    
    Constructor: Torus(position, major_radius, minor_radius, material)
    """
    def __init__(self, position, major_radius, minor_radius, material):
        super().__init__(position, material)
        self.major_radius = float(major_radius)  # R
        self.minor_radius = float(minor_radius)  # r
        self.type = "Torus"
        
    def solve_quartic(self, a, b, c, d, e):
        """Solve quartic equation ax^4 + bx^3 + cx^2 + dx + e = 0
        Returns list of real roots in ascending order"""
        # Use numpy's polynomial root finding
        coeffs = [a, b, c, d, e]
        roots = np.roots(coeffs)
        
        # Filter for real roots with small imaginary part
        real_roots = []
        for root in roots:
            if abs(root.imag) < 1e-10 and root.real > 1e-10:  # positive real roots
                real_roots.append(root.real)
        
        return sorted(real_roots)
    
    def ray_intersect(self, orig, dir):
        """Ray-Torus intersection using parametric equation.
        Torus equation: (sqrt(x^2 + z^2) - R)^2 + y^2 = r^2
        """
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        # Translate ray to torus local coordinates
        ray_orig = orig - self.position
        ray_dir = dir

        # Assign parameters early so the fast-reject can use them
        R = self.major_radius
        r = self.minor_radius

        # Fast reject with bounding sphere (radius = R + r)
        # If the ray doesn't intersect the outer sphere, it can't hit the torus.
        O = ray_orig
        tca_s = -np.dot(O, ray_dir)
        d2_s = np.dot(O, O) - tca_s * tca_s
        outer_r = (R + r)
        if d2_s > (outer_r * outer_r):
            return None
        
        # Ray equation: P(t) = ray_orig + t * ray_dir
        # Substitute into torus equation and expand to get quartic
        ox, oy, oz = ray_orig
        dx, dy, dz = ray_dir
        
        
        # Coefficients for the quartic equation at^4 + bt^3 + ct^2 + dt + e = 0
        # This comes from substituting P(t) into torus equation and expanding
        sum_d_sqr = dx*dx + dy*dy + dz*dz
        sum_o_sqr = ox*ox + oy*oy + oz*oz
        sum_od = ox*dx + oy*dy + oz*dz
        
        # Quartic coefficients
        a = sum_d_sqr * sum_d_sqr
        b = 4.0 * sum_d_sqr * sum_od
        c = 2.0 * sum_d_sqr * (sum_o_sqr - (R*R + r*r)) + 4.0 * sum_od * sum_od + 4.0 * R*R * (dy*dy)
        d = 4.0 * sum_od * (sum_o_sqr - (R*R + r*r)) + 8.0 * R*R * oy * dy
        e = (sum_o_sqr - (R*R + r*r)) * (sum_o_sqr - (R*R + r*r)) - 4.0 * R*R * (r*r - oy*oy)
        
        # Solve quartic equation
        roots = self.solve_quartic(a, b, c, d, e)
        
        if not roots:
            return None
            
        # Find the closest positive root
        t = roots[0] if roots[0] > 1e-6 else None
        if t is None:
            return None
            
        # Calculate intersection point
        P = ray_orig + t * ray_dir
        
        # Calculate normal at intersection point using correct torus normal formula
        x, y, z = P
        
        # For a torus with equation: (sqrt(x²+z²) - R)² + y² = r²
        # The gradient gives us the normal vector
        dist_from_center = np.sqrt(x*x + z*z)
        
        if dist_from_center < 1e-8:  # Special case: point on Y-axis
            # Use the direction towards/away from the Y-axis
            normal = np.array([1.0, 0.0, 0.0])  # arbitrary radial direction
        else:
            # Correct torus normal calculation
            # ∇F = (2(√(x²+z²) - R) * (x/√(x²+z²)), 2y, 2(√(x²+z²) - R) * (z/√(x²+z²)))
            radial_factor = 2.0 * (dist_from_center - R) / dist_from_center
            normal = np.array([radial_factor * x, 2.0 * y, radial_factor * z])
            
        # Normalize normal vector
        norm_length = np.linalg.norm(normal)
        if norm_length > 1e-8:
            normal = normal / norm_length
        else:
            # Fallback normal if calculation fails
            normal = np.array([0.0, 1.0, 0.0])
            
        # Transform back to world coordinates
        P_world = P + self.position
        
        return Intercept(
            point=P_world,
            normal=normal,
            distance=t,
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


class Cylinder(Shapes):
    """Cylinder with caps defined by position (center), axis direction, radius and height.
    
    Constructor: Cylinder(position, axis, radius, height, material)
    - position: center point of the cylinder
    - axis: direction vector (will be normalized) 
    - radius: radius of the cylinder
    - height: total height of the cylinder
    """
    def __init__(self, position, axis, radius, height, material):
        super().__init__(position, material)
        self.axis = np.array(axis, dtype=float)
        # Normalize axis
        axis_length = np.linalg.norm(self.axis)
        if axis_length > 1e-8:
            self.axis = self.axis / axis_length
        else:
            self.axis = np.array([0.0, 1.0, 0.0])  # default to Y-axis
            
        self.radius = float(radius)
        self.height = float(height)
        self.type = "Cylinder"
        
        # Pre-compute half-height for easier calculations
        self.half_height = self.height / 2.0
        
    def ray_intersect(self, orig, dir):
        """Ray-Cylinder intersection including side surface and caps."""
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        # Transform to cylinder local coordinates where axis is along Y
        # Vector from cylinder center to ray origin
        oc = orig - self.position
        
        # Project onto cylinder axis to get the Y-component in local space
        axis_proj_oc = np.dot(oc, self.axis)
        axis_proj_dir = np.dot(dir, self.axis)
        
        # Perpendicular components (in the XZ plane of cylinder space)
        perp_oc = oc - axis_proj_oc * self.axis
        perp_dir = dir - axis_proj_dir * self.axis
        
        candidates = []
        
        # 1. Intersect with cylindrical side surface
        # Equation: |perp_oc + t * perp_dir|² = radius²
        a = np.dot(perp_dir, perp_dir)
        b = 2.0 * np.dot(perp_oc, perp_dir)
        c = np.dot(perp_oc, perp_oc) - self.radius * self.radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant >= 0 and a > 1e-8:  # Ray intersects infinite cylinder
            sqrt_disc = np.sqrt(discriminant)
            t1 = (-b - sqrt_disc) / (2 * a)
            t2 = (-b + sqrt_disc) / (2 * a)
            
            for t in [t1, t2]:
                if t > 1e-6:  # Valid intersection
                    # Check if intersection is within cylinder height
                    y_intersect = axis_proj_oc + t * axis_proj_dir
                    if -self.half_height <= y_intersect <= self.half_height:
                        candidates.append((t, 'side', y_intersect))
        
        # 2. Intersect with caps (top and bottom)
        if abs(axis_proj_dir) > 1e-8:  # Ray not parallel to caps
            # Bottom cap (y = -half_height)
            t_bottom = (-self.half_height - axis_proj_oc) / axis_proj_dir
            if t_bottom > 1e-6:
                perp_at_bottom = perp_oc + t_bottom * perp_dir
                if np.dot(perp_at_bottom, perp_at_bottom) <= self.radius * self.radius:
                    candidates.append((t_bottom, 'bottom', -self.half_height))
            
            # Top cap (y = +half_height)
            t_top = (self.half_height - axis_proj_oc) / axis_proj_dir
            if t_top > 1e-6:
                perp_at_top = perp_oc + t_top * perp_dir
                if np.dot(perp_at_top, perp_at_top) <= self.radius * self.radius:
                    candidates.append((t_top, 'top', self.half_height))
        
        if not candidates:
            return None
            
        # Find closest intersection
        candidates.sort(key=lambda x: x[0])
        t, surface_type, y_local = candidates[0]
        
        # Compute intersection point
        P = orig + t * dir
        
        # Compute normal based on surface type
        if surface_type == 'side':
            # Normal on cylindrical surface (perpendicular to axis)
            local_radial = P - self.position - y_local * self.axis
            normal = local_radial / np.linalg.norm(local_radial)
        elif surface_type == 'top':
            normal = self.axis  # Points outward along axis
        else:  # surface_type == 'bottom'
            normal = -self.axis  # Points outward (opposite to axis)
        
        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            rayDirection=dir,
            obj=self,
            texCoords=None
        )


class Cone(Shapes):
    """Cone (right circular cone) defined by tip position, base center, and radius.
    
    Constructor: Cone(tip, base_center, radius, material)
    - tip: apex point of the cone
    - base_center: center of the circular base
    - radius: radius of the base circle
    """
    def __init__(self, tip, base_center, radius, material):
        # Position is the midpoint between tip and base for convenience
        midpoint = (np.array(tip) + np.array(base_center)) / 2.0
        super().__init__(midpoint, material)
        
        self.tip = np.array(tip, dtype=float)
        self.base_center = np.array(base_center, dtype=float)
        self.radius = float(radius)
        self.type = "Cone"
        
        # Calculate cone axis (from base to tip)
        self.axis = self.tip - self.base_center
        self.height = np.linalg.norm(self.axis)
        if self.height > 1e-8:
            self.axis = self.axis / self.height
        else:
            self.axis = np.array([0.0, 1.0, 0.0])
            
        # Cone angle for calculations
        self.cos_angle_sq = (self.height**2) / (self.height**2 + self.radius**2)
        
    def ray_intersect(self, orig, dir):
        """Ray-Cone intersection including conical surface and base."""
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        # Transform to cone local space (tip at origin, axis along positive direction)
        oc = orig - self.tip
        
        # Project onto cone axis
        axis_dot_oc = np.dot(self.axis, oc)
        axis_dot_dir = np.dot(self.axis, dir)
        
        candidates = []
        
        # 1. Intersect with conical surface
        # Cone equation: (oc + t*dir - proj_axis)² = (cos²θ) * (proj_axis)²
        # where proj_axis is the projection onto the cone axis
        
        # Coefficients for quadratic equation
        a = np.dot(dir, dir) - axis_dot_dir**2 * self.cos_angle_sq
        b = 2.0 * (np.dot(oc, dir) - axis_dot_oc * axis_dot_dir * self.cos_angle_sq)
        c = np.dot(oc, oc) - axis_dot_oc**2 * self.cos_angle_sq
        
        discriminant = b**2 - 4*a*c
        
        if discriminant >= 0 and abs(a) > 1e-8:
            sqrt_disc = np.sqrt(discriminant)
            t1 = (-b - sqrt_disc) / (2*a)
            t2 = (-b + sqrt_disc) / (2*a)
            
            for t in [t1, t2]:
                if t > 1e-6:
                    # Check if intersection is within cone bounds
                    P = orig + t * dir
                    tip_to_P = P - self.tip
                    proj_length = np.dot(tip_to_P, self.axis)
                    
                    # Must be between tip (0) and base (height)
                    if 0 <= proj_length <= self.height:
                        candidates.append((t, 'surface'))
        
        # 2. Intersect with circular base
        if abs(axis_dot_dir) > 1e-8:  # Ray not parallel to base
            # Base plane intersection
            t_base = (np.dot(self.base_center - orig, self.axis)) / axis_dot_dir
            
            if t_base > 1e-6:
                P_base = orig + t_base * dir
                # Check if point is within base circle
                base_to_P = P_base - self.base_center
                radial_dist_sq = np.dot(base_to_P, base_to_P) - (np.dot(base_to_P, self.axis))**2
                
                if radial_dist_sq <= self.radius**2:
                    candidates.append((t_base, 'base'))
        
        if not candidates:
            return None
            
        # Find closest intersection
        candidates.sort(key=lambda x: x[0])
        t, surface_type = candidates[0]
        
        # Compute intersection point and normal
        P = orig + t * dir
        
        if surface_type == 'surface':
            # Normal on conical surface
            tip_to_P = P - self.tip
            proj_length = np.dot(tip_to_P, self.axis)
            proj_point = self.tip + proj_length * self.axis
            
            # Radial component (perpendicular to axis)
            radial = P - proj_point
            radial_length = np.linalg.norm(radial)
            
            if radial_length > 1e-8:
                radial_unit = radial / radial_length
                # Normal combines radial and axial components
                axial_component = self.radius / self.height
                normal = radial_unit + axial_component * self.axis
                normal = normal / np.linalg.norm(normal)
            else:
                normal = -self.axis  # At tip, normal points back along axis
                
        else:  # surface_type == 'base'
            normal = -self.axis  # Base normal points away from tip
            
        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            rayDirection=dir,
            obj=self,
            texCoords=None
        )


class Pyramid(Shapes):
    """Triangular pyramid (tetrahedron) defined by apex and triangular base.
    
    Constructor: Pyramid(apex, base_vertices, material)
    - apex: tip point of the pyramid
    - base_vertices: list of 3 points forming the triangular base [v0, v1, v2]
    """
    def __init__(self, apex, base_vertices, material):
        # Position is centroid of all 4 vertices
        all_vertices = [apex] + list(base_vertices)
        centroid = np.mean(all_vertices, axis=0)
        super().__init__(centroid, material)
        
        self.apex = np.array(apex, dtype=float)
        self.base_v0 = np.array(base_vertices[0], dtype=float)
        self.base_v1 = np.array(base_vertices[1], dtype=float)
        self.base_v2 = np.array(base_vertices[2], dtype=float)
        self.type = "Pyramid"
        
        # Precompute base normal
        edge1 = self.base_v1 - self.base_v0
        edge2 = self.base_v2 - self.base_v0
        self.base_normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(self.base_normal)
        if norm > 1e-8:
            self.base_normal = self.base_normal / norm
        else:
            self.base_normal = np.array([0.0, 1.0, 0.0])
            
        # Ensure normal points away from apex
        apex_to_base = self.base_v0 - self.apex
        if np.dot(self.base_normal, apex_to_base) < 0:
            self.base_normal = -self.base_normal
    
    def point_in_triangle(self, point, v0, v1, v2):
        """Check if point lies inside triangle using barycentric coordinates."""
        # Compute vectors
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        v0p = point - v0
        
        # Compute dot products
        dot00 = np.dot(v0v2, v0v2)
        dot01 = np.dot(v0v2, v0v1)
        dot02 = np.dot(v0v2, v0p)
        dot11 = np.dot(v0v1, v0v1)
        dot12 = np.dot(v0v1, v0p)
        
        # Compute barycentric coordinates
        inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v <= 1)
    
    def intersect_triangle(self, orig, dir, v0, v1, v2, normal):
        """Intersect ray with triangle using Möller-Trumbore algorithm."""
        edge1 = v1 - v0
        edge2 = v2 - v0
        h = np.cross(dir, edge2)
        a = np.dot(edge1, h)
        
        if abs(a) < 1e-6:  # Ray parallel to triangle
            return None
            
        f = 1.0 / a
        s = orig - v0
        u = f * np.dot(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
            
        q = np.cross(s, edge1)
        v = f * np.dot(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None
            
        t = f * np.dot(edge2, q)
        
        if t > 1e-6:
            return t
        return None
        
    def ray_intersect(self, orig, dir):
        """Ray-Pyramid intersection with 4 triangular faces."""
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        candidates = []
        
        # Face 1: Base triangle
        t = self.intersect_triangle(orig, dir, self.base_v0, self.base_v1, self.base_v2, self.base_normal)
        if t is not None:
            candidates.append((t, 'base', self.base_normal))
            
        # Face 2: Side triangle (apex, v0, v1)
        edge1 = self.base_v1 - self.apex
        edge2 = self.base_v0 - self.apex
        side_normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(side_normal)
        if norm > 1e-8:
            side_normal = side_normal / norm
            t = self.intersect_triangle(orig, dir, self.apex, self.base_v0, self.base_v1, side_normal)
            if t is not None:
                candidates.append((t, 'side1', side_normal))
        
        # Face 3: Side triangle (apex, v1, v2)
        edge1 = self.base_v2 - self.apex
        edge2 = self.base_v1 - self.apex
        side_normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(side_normal)
        if norm > 1e-8:
            side_normal = side_normal / norm
            t = self.intersect_triangle(orig, dir, self.apex, self.base_v1, self.base_v2, side_normal)
            if t is not None:
                candidates.append((t, 'side2', side_normal))
        
        # Face 4: Side triangle (apex, v2, v0)
        edge1 = self.base_v0 - self.apex
        edge2 = self.base_v2 - self.apex
        side_normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(side_normal)
        if norm > 1e-8:
            side_normal = side_normal / norm
            t = self.intersect_triangle(orig, dir, self.apex, self.base_v2, self.base_v0, side_normal)
            if t is not None:
                candidates.append((t, 'side3', side_normal))
        
        if not candidates:
            return None
            
        # Find closest intersection
        candidates.sort(key=lambda x: x[0])
        t, face_type, normal = candidates[0]
        
        P = orig + t * dir
        
        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            rayDirection=dir,
            obj=self,
            texCoords=None
        )


class Ellipsoid(Shapes):
    """Ellipsoid defined by center position and three semi-axes (a, b, c).
    
    Constructor: Ellipsoid(position, semi_axes, material)
    - position: center point [x, y, z]
    - semi_axes: [a, b, c] where a=x-axis, b=y-axis, c=z-axis semi-axis lengths
    """
    def __init__(self, position, semi_axes, material):
        super().__init__(position, material)
        self.a, self.b, self.c = semi_axes
        self.type = "Ellipsoid"
        
    def ray_intersect(self, orig, dir):
        # Transform ray to ellipsoid space where it becomes a unit sphere
        # Ellipsoid equation: (x/a)² + (y/b)² + (z/c)² = 1
        
        orig = np.array(orig, dtype=float)
        dir = np.array(dir, dtype=float)
        
        # Translate origin to ellipsoid center
        oc = orig - self.position
        
        # Scale by inverse of semi-axes
        scaled_oc = oc / [self.a, self.b, self.c]
        scaled_dir = dir / [self.a, self.b, self.c]
        
        # Now solve for unit sphere: |scaled_point|² = 1
        # Quadratic equation: at² + bt + c = 0
        a = np.dot(scaled_dir, scaled_dir)
        b = 2.0 * np.dot(scaled_oc, scaled_dir)
        c = np.dot(scaled_oc, scaled_oc) - 1.0
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None
            
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        
        # Choose nearest positive intersection
        t = None
        if t1 > 0.001:
            t = t1
        elif t2 > 0.001:
            t = t2
        else:
            return None
            
        # Calculate intersection point and normal
        point = orig + t * dir
        
        # Normal vector: gradient of ellipsoid equation at point
        local_point = point - self.position
        normal = np.array([
            2 * local_point[0] / (self.a * self.a),
            2 * local_point[1] / (self.b * self.b), 
            2 * local_point[2] / (self.c * self.c)
        ])
        normal = normal / np.linalg.norm(normal)
        
        return Intercept(
            point=point,
            normal=normal,
            distance=t,
            rayDirection=dir,
            obj=self,
            texCoords=None
        )