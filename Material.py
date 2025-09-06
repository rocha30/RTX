import numpy as np
from intercept import *
from MathLib import *
from refractionFunctions import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(self, diffuse=[1,1,1], spec=1.0, ks=0, ior =1 ,texture = None,  matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.ks = ks
        self.texture = texture
        self.matType = matType

    def GetSurfaceColor(self, intercept, renderer, recursion=0):
        shadowIntercept = None
        lightColor = [0, 0, 0]
        specColor = [0, 0, 0]
        textureColor = [0,0,0]
        reflectColor = [0, 0, 0]
        refractColor = [0,0,0]
        finalColor = self.diffuse
        
        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i]* textureColor[i] for i in range (3)]


        for light in renderer.lights:
               
            if light.lightType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept == None:
                
                specColor = [(specColor[i] + light.GetSpecularColor(intercept, renderer.camera.translation)[i]) for i in range(3)]
                
                if self.matType == OPAQUE: 
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]
                    
        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)

            reflectIntercept= renderer.glCastRay(intercept.point, reflect, intercept.obj,recursion + 1)
            
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

                
        elif self.matType == TRANSPARENT:
            #se revusa de donde viene el rayo
            outside = np.dot(intercept.normal, intercept.rayDirection) < 0
            #agregar el bias para evitar errores de precision
            bias = [i * 0.001 for i in intercept.normal]
            
            #refleccion 
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectOrig = np.add(intercept.point, bias) if outside else np.subtract(intercept.point, bias)
            reflectIntercept= renderer.glCastRay(reflectOrig, reflect, None,recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            #Refraccion
            if not totalInternalReflection(intercept.normal, intercept.rayDirection,1.0, self.ior):  
                refract = refractVector(intercept.normal, intercept.rayDirection,1.0 , self.ior)
                refractOrig = np.subtract(intercept.point, bias) if outside else np.add(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)

                if refractIntercept != None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, refract)

            #Usamos fresnel 
            # Kr, Kt = fresnel(intercept.normal, intercept.rayDirection , 1.0, self.ior)
            # reflectColor = [ks * ]
            # refractColor = 

        # Aplicar el color difuso del material
        # diffuse * (Light + Reflect + Refract) + specColor
        finalColor = [ finalColor[i]* (lightColor[i] + reflectColor[i] + refractColor[i]) for i in range(3)]
        finalColor = [(finalColor[i] + specColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        
        
        
        return finalColor


red_material = Material(diffuse=[1, 0, 0], spec = 64, ks=0.2)
green_material = Material(diffuse=[0, 1, 0], spec = 64, ks=0.2)
mirror_material = Material(diffuse=[0.9,0.9,0.9], matType=REFLECTIVE)
glass = Material(ior = 1.5, matType=TRANSPARENT)
marble = Material(diffuse=[0.85,0.85,0.85], spec = 32, ks=0.25, matType=REFLECTIVE)

"""
Para el phong se necesita calcular 
P=punto de interseccion del rayo con el objeto
N=normal en el punto de interseccion (normalizado)
L=direccion de la luz (normalizado)
V=direccion de la camara (normalizado)
R=reflexion de 'L' respecto a 'N'
"""