import numpy as np
from intercept import *


class Material(object):
    def __init__(self, diffuse=[1,1,1], spec=1.0, ks=0):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
    
    def GetSurfaceColor(self, intercept, renderer):
        shadowIntercept = None
        lightColor = [0, 0, 0]
        specColor = [0, 0, 0]

        for light in renderer.lights:
               
            if light.lightType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept == None:
                lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]
                
                specColor = [(specColor[i] + light.GetSpecularColor(intercept, renderer.camera.translation)[i]) for i in range(3)]

        # Aplicar el color difuso del material
        finalColor = [(self.diffuse[i] * lightColor[i] + specColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        
        
        
        return finalColor


red_material = Material(diffuse=[1, 0, 0], spec = 64, ks=0.2)
green_material = Material(diffuse=[0, 1, 0], spec = 64, ks=0.2)

"""
Para el phong se necesita calcular 
P=punto de interseccion del rayo con el objeto
N=normal en el punto de interseccion (normalizado)
L=direccion de la luz (normalizado)
V=direccion de la camara (normalizado)
R=reflexion de 'L' respecto a 'N'
"""