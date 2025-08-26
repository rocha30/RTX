import numpy as np

class Material:
    def __init__(self, ka, kd, ks, shininess, color):
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.shininess = shininess
        self.color = np.array(color)


    def phong_lighting(P, N, V, light_pos, light_intensity, material):

        L = (light_pos - P) #direccion de la luz menos el punto de interseccion. 
        L = L / np.linalg.norm(L) #normalizada

        R = 2 * np.dot(N, L) * N - L #reflexion de L respecto a N
        R = R / np.linalg.norm(R) #normalizada

        ambient = material.ka * light_intensity
        diffuse = material.kd * light_intensity * max(0, np.dot(N, L))
        specular = material.ks * light_intensity * (max(0, np.dot(R, V)) ** material.shininess)

        return material.color * (ambient + diffuse + specular)
    
"""
Para el phong se necesita calcular 
P=punto de interseccion del rayo con el objeto
N=normal en el punto de interseccion (normalizado)
L=direccion de la luz (normalizado)
V=direccion de la camara (normalizado)
R=reflexion de 'L' respecto a 'N'
"""