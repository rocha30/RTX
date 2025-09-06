import numpy as np
from intercept import *
from MathLib import *
from refractionFunctions import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(self, diffuse=[1,1,1], spec=1.0, ks=0, ior = 1.0 ,texture = None,  matType = OPAQUE):
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
            #se revisa de donde viene el rayo
            outside = np.dot(intercept.normal, intercept.rayDirection) < 0
            #agregar el bias para evitar errores de precision
            bias = [i * 0.001 for i in intercept.normal]
            
            #refleccion 
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectOrig = np.add(intercept.point, bias) if outside else np.subtract(intercept.point, bias)
            reflectIntercept= renderer.glCastRay(reflectOrig, reflect, None, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            #Refraccion
            if not totalInternalReflection(intercept.normal, intercept.rayDirection,1.0, self.ior):  
                refract = refractVector(intercept.normal, intercept.rayDirection, 1.0 , self.ior)
                refractOrig = np.subtract(intercept.point, bias) if outside else np.add(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)

                if refractIntercept != None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, refract)

                #Usamos fresnel
                ks, kt = fresnel(intercept.normal, intercept.rayDirection , 1.0, self.ior);
                reflectColor = [i * ks for i in reflectColor]
                refractColor = [i * kt for i in refractColor]

        # Aplicar el color difuso del material
        # diffuse * (Light + Reflect + Refract) + specColor
        finalColor = [ finalColor[i] * (lightColor[i] + reflectColor[i] + refractColor[i]) for i in range(3)]
        finalColor = [(finalColor[i] + specColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        
        
        
        return finalColor


# Opacos
matte_red = Material(
    diffuse=[0.85, 0.15, 0.15],  # rojo mate
    spec=8,                      # highlight suave
    ks=0.0,
    matType=OPAQUE
)

glossy_blue = Material(
    diffuse=[0.15, 0.25, 0.90],  # azul saturado
    spec=32,                     # un poco más brillante
    ks=0.0,
    matType=OPAQUE
)

# Reflectivos
polished_gold = Material(
    diffuse=[0.35, 0.28, 0.06], 
    spec=96,
    ks=0.90, 
    matType=REFLECTIVE)

lacquer_red = Material(
    diffuse=[0.40, 0.05, 0.05],  # “capa base” rojiza
    spec=64,                     # pulido
    ks=0.65,                     # mezcla reflejo/undercoat
    matType=REFLECTIVE
)

# Transparentes
clear_glass = Material(
    diffuse=[1.0, 1.0, 1.0],     # sin tinte
    spec=64,                     # pulido
    ks=0.0,
    ior=1.50,                    # vidrio
    matType=TRANSPARENT
)

green_glass = Material(
    diffuse=[0.85, 1.00, 0.85],  # leve tinte verdoso (aplica a la parte transmitida)
    spec=64,
    ks=0.0,
    ior=1.52,                    # vidrio cal-soda típico
    matType=TRANSPARENT
)



"""
Para el phong se necesita calcular 
P=punto de interseccion del rayo con el objeto
N=normal en el punto de interseccion (normalizado)
L=direccion de la luz (normalizado)
V=direccion de la camara (normalizado)
R=reflexion de 'L' respecto a 'N'
"""