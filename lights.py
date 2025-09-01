import numpy as np
from MathLib import *
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

            dir = [(i*-1) for i in self.direction]
            surfaceIntensity = np.dot(intercept.normal, dir)
            surfaceIntensity = max(0, min(1, surfaceIntensity))
            lightColor = [(i* surfaceIntensity) for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color
        
        if intercept: 
            dir = -self.direction
            reflect = self.reflectVector(intercept.normal, dir)

            #SpecIntensity = ((V o R) ^ spec) * ks
            viewDir = viewPos - intercept.point
            viewDir /= np.linalg.norm(viewDir)

            specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec 
            specIntensity *= intercept.obj.material.ks
            specIntensity *= self.intensity
            specColor = [(i * specIntensity) for i in specColor]

        return specColor