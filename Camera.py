import numpy as np
from math import tan, pi, cos, sin, radians


class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 3.0])
        self.target = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])
        
        # Añadir translation para compatibilidad con el renderer
        self.translation = self.position
        
        self.fov = 45  # Field of view in degrees
        self.aspect = 1  # Aspect ratio
        self.near = 0.1  # Near clipping plane
        self.far = 50.0  # Far clipping plane
        
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 720
        self.viewport_height = 720
        
        

    def set_position(self, x, y, z):
        """Establece la posición de la cámara"""
        self.position = np.array([x, y, z])
        self.translation = -self.position  # Mantener sincronizado

    def set_target(self, x, y, z):
        """Establece el objetivo (punto al que mira la cámara)"""
        self.target = np.array([x, y, z])

    def set_up(self, x, y, z):
        """Establece el vector up de la cámara"""
        self.up = np.array([x, y, z])

    def set_projection(self, fov, aspect, near, far):
        """Establece los parámetros de proyección"""
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    def set_viewport(self, x, y, width, height):
        """Establece los parámetros del viewport"""
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height

    def get_view_matrix(self):
        """Obtiene la matriz de vista (lookAt)"""
        return self.view_matrix(self.position, self.target, self.up)

    def get_projection_matrix(self):
        """Obtiene la matriz de proyección perspectiva"""
        return self.projection_matrix(self.fov, self.aspect, self.near, self.far)

    def get_viewport_matrix(self):
        """Obtiene la matriz de viewport"""
        return self.viewport_matrix(self.viewport_x, self.viewport_y,
                                   self.viewport_width, self.viewport_height)

    def view_matrix(self, position, target, up):
        """Crea una matriz de vista usando lookAt"""
        # Calcular los vectores de la cámara
        forward = target - position
        forward = forward / np.linalg.norm(forward)
        
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        
        up_corrected = np.cross(right, forward)
        
        # Crear matriz de rotación
        rotation_matrix = np.array([
            [right[0], up_corrected[0], -forward[0], 0],
            [right[1], up_corrected[1], -forward[1], 0],
            [right[2], up_corrected[2], -forward[2], 0],
            [0, 0, 0, 1]
        ])
        
        # Crear matriz de traslación
        translation_matrix = np.array([
            [1, 0, 0, -position[0]],
            [0, 1, 0, -position[1]],
            [0, 0, 1, -position[2]],
            [0, 0, 0, 1]
        ])
        
        # Combinar rotación y traslación
        view_matrix = np.dot(rotation_matrix, translation_matrix)
        return view_matrix

    def projection_matrix(self, fov, aspect, near, far):
        """Crea una matriz de proyección perspectiva"""
        fov_rad = radians(fov)
        f = 1.0 / tan(fov_rad / 2.0)
        
        return np.array([
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ])

    def viewport_matrix(self, x, y, width, height):
        """Crea una matriz de viewport"""
        return np.array([
            [width / 2, 0, 0, x + width / 2],
            [0, height / 2, 0, y + height / 2],
            [0, 0, 0.5, 0.5],
            [0, 0, 0, 1]
        ])

    def move_forward(self, distance):
        """Mueve la cámara hacia adelante"""
        forward = self.target - self.position
        forward = forward / np.linalg.norm(forward)
        self.set_position(*(self.position + forward * distance))

    def move_backward(self, distance):
        """Mueve la cámara hacia atrás"""
        self.move_forward(-distance)

    def move_left(self, distance):
        """Mueve la cámara hacia la izquierda"""
        forward = self.target - self.position
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, self.up)
        right = right / np.linalg.norm(right)
        self.set_position(*(self.position - right * distance))

    def move_right(self, distance):
        """Mueve la cámara hacia la derecha"""
        self.move_left(-distance)

    def move_up(self, distance):
        """Mueve la cámara hacia arriba"""
        self.set_position(*(self.position + self.up * distance))

    def move_down(self, distance):
        """Mueve la cámara hacia abajo"""
        self.move_up(-distance)

    def orbit(self, angle_x, angle_y, radius=None):
        """Orbita alrededor del target"""
        if radius is None:
            radius = np.linalg.norm(self.position - self.target)
        
        # Convertir ángulos a radianes
        angle_x = radians(angle_x)
        angle_y = radians(angle_y)
        
        # Calcular nueva posición
        x = self.target[0] + radius * cos(angle_y) * sin(angle_x)
        y = self.target[1] + radius * sin(angle_y)
        z = self.target[2] + radius * cos(angle_y) * cos(angle_x)
        
        self.set_position(x, y, z)

    def look_at(self, target_x, target_y, target_z):
        """Hace que la cámara mire hacia un punto específico"""
        self.set_target(target_x, target_y, target_z)

    def get_forward_vector(self):
        """Obtiene el vector hacia adelante de la cámara"""
        forward = self.target - self.position
        return forward / np.linalg.norm(forward)

    def get_right_vector(self):
        """Obtiene el vector hacia la derecha de la cámara"""
        forward = self.get_forward_vector()
        right = np.cross(forward, self.up)
        return right / np.linalg.norm(right)

    def get_up_vector(self):
        """Obtiene el vector hacia arriba de la cámara"""
        forward = self.get_forward_vector()
        right = self.get_right_vector()
        return np.cross(right, forward)

    def __str__(self):
        """Representación en string de la cámara"""
        return f"Camera(pos={self.position}, target={self.target}, up={self.up}, fov={self.fov})"

    def __repr__(self):
        return self.__str__()