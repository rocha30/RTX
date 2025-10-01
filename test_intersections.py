import numpy as np
from figures import OBB, Torus
from Material import matte_red

print('Testing OBB and Torus intersections')

# OBB centered at (0,0,-5) axis-aligned, extents 1
obb = OBB(center=[0,0,-5], axes=[[1,0,0],[0,1,0],[0,0,1]], extents=[1,1,1], material=matte_red)
# Torus centered at (2.5,0,-5) with major 1.5, minor 0.5
torus = Torus(position=[2.5,0,-5], major_radius=1.5, minor_radius=0.5, material=matte_red)

rays = [
    ("obb_center", np.array([0.0,0.0,0.0]), np.array([0.0,0.0,-1.0])),
    ("obb_miss", np.array([3.0,0.0,0.0]), np.array([0.0,0.0,-1.0])),
    ("torus_hit", np.array([2.5,0.0,0.0]), np.array([0.0,0.0,-1.0])),
    ("torus_miss", np.array([0.0,5.0,0.0]), np.array([0.0,0.0,-1.0]))
]

for name, orig, dir in rays:
    dir = dir / np.linalg.norm(dir)
    if name.startswith('obb'):
        hit = obb.ray_intersect(orig, dir)
    else:
        hit = torus.ray_intersect(orig, dir)
    print(name, 'hit=', hit is not None)
    if hit:
        print('  point', hit.point, 'normal', hit.normal, 'dist', hit.distance)
