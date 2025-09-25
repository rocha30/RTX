import numpy as np
from MathLib import * 
from math import cos , pi

class Light(object):
    def __init__(self, color = [1,1,1], intensity = 1.0, lightType = 'None'):
        self.color = color
        self.intensity = intensity
        self.lightType = lightType

    def GetLightColor(self, intercept = None):
        return[(i * self.intensity) for i in self.color]

    def GetSpecularColor(self, intercept, viewPos):
        return [0,0,0]

    def reflectVector( self, normal, lightDir):
        normal = normal/ np.linalg.norm(normal)
        lightDir = lightDir/ np.linalg.norm(lightDir)
        return lightDir - 2 * np.dot(lightDir, normal) * normal


class AmbientLight(Light):
    def __init__(self, color = [1,1,1], intensity = 0.1):
        super().__init__(color, intensity, "Ambient")
        

class DirectionalLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0, direction = [0,-1,0]):
        super().__init__(color, intensity, 'Directional')
        self.direction = direction / np.linalg.norm(direction)

    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor()

        if intercept: 
        #surfaceIntensity = NORMAL DOT -LIGHT

            dir = [(i * -1) for i in self.direction]
            surfaceIntensity = np.dot(intercept.normal, dir)
            surfaceIntensity = max(0, min(1, surfaceIntensity))
            lightColor = [(i * surfaceIntensity) for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color
        #R = 2 * (N o L) * N - L --> Funcion de relfejo

        if intercept:
            dir = [(i * -1) for i in self.direction]
            reflect = reflectVector(intercept.normal, dir)

            #SpecIntensity = ((V o R) ^ spec) * ks
            viewDir = np.subtract(viewPos, intercept.point)
            viewDir /= np.linalg.norm(viewDir)

            specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec 
            specIntensity *= intercept.obj.material.ks
            specIntensity *= self.intensity
            specColor = [(i * specIntensity) for i in specColor]

        return specColor


class PointLight (Light):
    def __init__(self, color = [1,1,1], intensity = 1.0, position = [0,0,0]):
        super().__init__(color, intensity, 'Point')
        self.position = position
        self.lightType = 'Point'
    
    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor()
        if intercept:
            dir = np.subtract(self.position, intercept.point)
            R = np.linalg.norm(dir)
            dir /= R

            surfaceIntensity = np.dot(intercept.normal, dir)

            # ley de cuadrados inversos
            # atenuacion = intensity  / R^2
            #revisar division por cero
            if R != 0:
                surfaceIntensity /= R**2 
                
                
            surfaceIntensity = max(0, min(1, surfaceIntensity))
            lightColor = [(i * surfaceIntensity) for i in lightColor]
            
        return lightColor

    
    def GetSpecularColor(self, intercept, viewPos):
        specColor = super().GetLightColor()
        #R = 2 * (N o L) * N - L --> Funcion de relfejo

        if intercept:
            dir = np.subtract(self.position, intercept.point)
            R = np.linalg.norm(dir)
            dir /= R

            reflect = reflectVector(intercept.normal, dir)
            
            
            viewDir = np.subtract(viewPos, intercept.point)
            viewDir /= np.linalg.norm(viewDir)

            # ley de cuadrados inversos
            # atenuacion = intensity  / R^2
            #revisar division por cero

            specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
            specIntensity *= self.intensity
            
            if R != 0:
                specIntensity /= R**2
                
            specColor = [(i * specIntensity) for i in specColor]

        return specColor
    
    

class SpotLight (PointLight):
    def __init__(self, color = [1,1,1], intensity = 1.0, position = [0,0,0], direction = [0,-1,0], innerAngle = 50, outerAngle = 60):
        super().__init__(color, intensity, position )
        self.direction = direction / np.linalg.norm(direction)
        self.innerAngle = innerAngle #angulos en radianes
        self.outerAngle = outerAngle
        self.lightType = 'Spot'
        
    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor(intercept)

        lightColor = [(i * self.EdgeAttenuation(intercept)) for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = super().GetSpecularColor(intercept, viewPos)
        specColor = [(i * self.EdgeAttenuation(intercept)) for i in specColor]
        return specColor

    def EdgeAttenuation(self, intercept = None):
        if intercept == None:
            return 0
        
        wi = np.subtract(self.position, intercept.point)
        wi /= np.linalg.norm(wi)

        innerAngleRad = self.innerAngle * pi / 180
        outerAngleRad = self.outerAngle * pi / 180

        attenuation = (-np.dot(self.direction, wi) - cos(outerAngleRad)) / (cos(innerAngleRad) - cos(outerAngleRad))
        attenuation = max(0, min(1, attenuation))
        
        return attenuation
