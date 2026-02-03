import numpy as np
from intercept import *
from MathLib import *
from refractionFunctions import *
from BMPTexture import BMPTexture

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
EMISSIVE = 3  # Nuevo tipo de material emisivo


class Material(object):
    def __init__(self, diffuse=[1,1,1], spec=1.0, ks=0, ior = 1.0 ,texture = None, matType = OPAQUE, emission=[0,0,0]):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.ks = ks
        self.texture = texture
        self.matType = matType
        self.emission = emission  # Color de emisión para materiales emisivos

    def GetSurfaceColor(self, intercept, renderer, recursion=0):
        shadowIntercept = None
        lightColor = [0, 0, 0]
        specColor = [0, 0, 0]
        textureColor = [0,0,0]
        reflectColor = [0, 0, 0]
        refractColor = [0,0,0]
        finalColor = self.diffuse
        
        # Si es material emisivo, empezar con su color de emisión
        if self.matType == EMISSIVE:
            lightColor = self.emission[:]
        
        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            if textureColor:  # Solo aplicar si se obtuvo un color válido
                finalColor = [finalColor[i] * textureColor[i] for i in range(3)]


        for light in renderer.lights:

            if light.lightType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            elif light.lightType == "Point" or light.lightType == "Spot":
                lightDir = np.subtract(light.position, intercept.point)
                R = np.linalg.norm(lightDir)
                lightDir /= R
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)
    
                if shadowIntercept != None:
                    if shadowIntercept.distance > R:
                        shadowIntercept = None
                    
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

# Materiales más suaves y neutros
soft_white = Material(
    diffuse=[0.9, 0.9, 0.9],     # blanco suave
    spec=16,
    ks=0.0,
    matType=OPAQUE
)

warm_gray = Material(
    diffuse=[0.7, 0.65, 0.6],    # gris cálido
    spec=8,
    ks=0.0,
    matType=OPAQUE
)

light_beige = Material(
    diffuse=[0.8, 0.75, 0.7],    # beige claro
    spec=12,
    ks=0.0,
    matType=OPAQUE
)

soft_gold = Material(
    diffuse=[0.6, 0.5, 0.3],     # dorado suave
    spec=32,
    ks=0.3,
    matType=REFLECTIVE
)

pale_blue = Material(
    diffuse=[0.8, 0.85, 0.9],    # azul pálido
    spec=16,
    ks=0.0,
    matType=OPAQUE
)

# ===== MATERIALES PARA ESCENA COMPLEJA LAB FINAL =====

# Cristales transparentes con diferentes IOR
crystal_clear = Material(
    diffuse=[1.0, 1.0, 1.0],     # cristal puro
    spec=128,
    ks=0.0,
    ior=1.52,                    # vidrio de cuarzo
    matType=TRANSPARENT
)

crystal_red = Material(
    diffuse=[1.0, 0.9, 0.9],     # ligero tinte rojo
    spec=128,
    ks=0.0,
    ior=1.54,                    # vidrio con plomo
    matType=TRANSPARENT
)

crystal_green = Material(
    diffuse=[0.9, 1.0, 0.9],     # tinte verde
    spec=128,
    ks=0.0,
    ior=1.53,
    matType=TRANSPARENT
)

# Metales brillantes
polished_silver = Material(
    diffuse=[0.75, 0.75, 0.8],   # plata pulida
    spec=128,
    ks=0.95,
    matType=REFLECTIVE
)

brass_shiny = Material(
    diffuse=[0.7, 0.6, 0.25],    # latón brillante
    spec=96,
    ks=0.85,
    matType=REFLECTIVE
)

# Material emisivo naranja
emissive_orange = Material(
    diffuse=[1.0, 0.6, 0.2],     # base naranja
    spec=32,
    ks=0.0,
    matType=EMISSIVE,
    emission=[1.0, 0.5, 0.1]     # luz naranja intensa
)

# Materiales mate y texturizados
matte_black = Material(
    diffuse=[0.05, 0.05, 0.05],  # negro mate
    spec=4,
    ks=0.0,
    matType=OPAQUE
)

wood_dark = Material(
    diffuse=[0.4, 0.25, 0.15],   # madera oscura
    spec=8,
    ks=0.1,                      # ligero brillo
    matType=OPAQUE
)

wood_light = Material(
    diffuse=[0.6, 0.45, 0.3],    # madera clara
    spec=8,
    ks=0.05,
    matType=OPAQUE
)

sand_texture = Material(
    diffuse=[0.8, 0.75, 0.6],    # arena
    spec=4,
    ks=0.0,
    texture=BMPTexture('sand.bmp'),  # Usando la textura del environment map
    matType=OPAQUE
)

rock_dark = Material(
    diffuse=[0.3, 0.3, 0.35],    # piedra oscura
    spec=8,
    ks=0.05,
    matType=OPAQUE
)

water_material = Material(
    diffuse=[0.8, 0.9, 1.0],     # agua azulada
    spec=64,
    ks=0.0,
    ior=1.33,                    # índice del agua
    matType=TRANSPARENT
)

# Material para vitrina (cristal con alta transparencia)
display_glass = Material(
    diffuse=[1.0, 1.0, 1.0],     # completamente transparente
    spec=128,
    ks=0.0,
    ior=1.51,                    # vidrio común
    matType=TRANSPARENT
)

# Materiales metálicos adicionales
copper_aged = Material(
    diffuse=[0.5, 0.3, 0.2],     # cobre envejecido
    spec=64,
    ks=0.7,
    matType=REFLECTIVE
)

steel_brushed = Material(
    diffuse=[0.6, 0.6, 0.65],    # acero cepillado
    spec=96,
    ks=0.8,
    matType=REFLECTIVE
)

# Material púrpura/gris para toro
torus_purple = Material(
    diffuse=[0.5, 0.4, 0.6],     # púrpura grisáceo
    spec=64,
    ks=0.6,
    matType=REFLECTIVE
)

# Material de cristal puro sin reflejos (solo transparente)
glass = Material(
    diffuse=[1.0, 1.0, 1.0],     # completamente blanco
    spec=0,                      # sin brillo especular
    ks=0.0,                      # sin reflectividad
    ior=1.001,                   # muy cerca del aire para evitar refracción visible
    matType=TRANSPARENT          # transparente pero sin efectos visuales
)

# Material de vitrina más estable
vitrina_glass = Material(
    diffuse=[0.95, 0.98, 1.0],   # ligerísimo tinte azul (como vidrio real)
    spec=32,                     # un poco de brillo
    ks=0.1,                      # muy poca reflectividad
    ior=1.1,                     # refracción mínima pero estable
    matType=TRANSPARENT
)

# Material de vitrina con tinte azul visible
vitrina_glass = Material(
    diffuse=[0.85, 0.9, 0.95],  # Color azul muy claro pero visible
    spec=0.2,   # Reflexión baja
    ks=0.1,     # Componente especular bajo
    matType=OPAQUE,  # Completamente opaco para probar
    ior=1.0     # Sin refracción para simplificar
)

# Materiales adicionales para las figuras
mirror = Material(
    diffuse=[0.9, 0.9, 0.9],
    spec=0.9,
    ks=0.8,
    matType=REFLECTIVE,
    ior=1.0
)

metal = Material(
    diffuse=[0.7, 0.7, 0.8],
    spec=0.8,
    ks=0.6,
    matType=OPAQUE,
    ior=1.0
)

red_plastic = Material(
    diffuse=[0.8, 0.2, 0.2],
    spec=0.4,
    ks=0.3,
    matType=OPAQUE,
    ior=1.0
)

# Material de madera con textura para el pedestal
wood_textured = Material(
    diffuse=[0.6, 0.4, 0.2],    # Color base de madera
    spec=0.2,                   # Menos reflexión para madera
    ks=0.1,                     # Menos especular
    texture=BMPTexture('wood.bmp'),  # Usando textura existente
    matType=OPAQUE,
    ior=1.0
)



"""
Para el phong se necesita calcular 
P=punto de interseccion del rayo con el objeto
N=normal en el punto de interseccion (normalizado)
L=direccion de la luz (normalizado)
V=direccion de la camara (normalizado)
R=reflexion de 'L' respecto a 'N'
"""