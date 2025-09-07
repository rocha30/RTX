# RTX - Python Ray Tracer

Un motor de ray tracing implementado en Python usando Pygame, capaz de renderizar escenas 3D con iluminación realista, reflexiones, refracciones y diferentes tipos de materiales.

![Ejemplo de renderizado](https://github.com/rocha30/RTX/blob/Lab6/6%20_Spheres.png)

## Características

### 🎨 Materiales Avanzados
- **Materiales Opacos**: Superficies mate con diferentes niveles de rugosidad
- **Materiales Reflectivos**: Metales pulidos como oro con reflexiones especulares
- **Materiales Transparentes**: Vidrio con refracción y diferentes índices de refracción
- **Soporte para Texturas**: Carga de texturas BMP para mapeo de superficies

### 💡 Sistema de Iluminación
- **Luz Ambiental**: Iluminación global uniforme
- **Luz Direccional**: Simulación de luz solar con sombras
- **Modelo de Phong**: Cálculo de iluminación especular y difusa

### 🌍 Efectos Ambientales
- **Environment Mapping**: Reflexiones del entorno usando texturas panorámicas
- **Sombras**: Cálculo de sombras proyectadas con ray tracing
- **Reflexiones Recursivas**: Múltiples rebotes de luz para efectos realistas

### 🔧 Funcionalidades Técnicas
- **Anti-aliasing**: Mejora de calidad visual mediante supersampling
- **Refracción con Ley de Snell**: Comportamiento físicamente correcto del vidrio
- **Reflexión Interna Total**: Efectos ópticos avanzados en materiales transparentes

## Estructura del Proyecto

```
RTX/
├── RayTracer.py          # Archivo principal de ejecución
├── gl.py                 # Motor de renderizado principal
├── Camera.py             # Sistema de cámara y proyección
├── Material.py           # Definición de materiales y shading
├── figures.py            # Geometría 3D (esferas, planos, etc.)
├── lights.py             # Sistema de iluminación
├── intercept.py          # Cálculos de intersección rayo-objeto
├── MathLib.py            # Funciones matemáticas auxiliares
├── refractionFunctions.py # Cálculos de refracción y reflexión
├── BMPTexture.py         # Carga y manejo de texturas BMP
├── BMP_Writer.py         # Exportación de imágenes en formato BMP
└── Fondo.bmp            # Texture de environment map
```

## Instalación

### Requisitos
- Python 3.8+
- Pygame
- NumPy

### Instalación de dependencias
```bash
pip install pygame numpy
```

## Uso

### Ejecución Básica
```bash
python RayTracer.py
```

### Personalización de Escena

El archivo `RayTracer.py` contiene la configuración de la escena. Puedes modificar:

```python
# Configuración de pantalla
width = 720
height = 720

# Agregar objetos a la escena
rend.scene.append(Sphere(
    position=[x, y, z], 
    radius=r, 
    material=material_type
))

# Configurar iluminación
rend.lights.append(DirectionalLight(
    direction=[-1, -1, -1], 
    intensity=1
))
```

## Materiales Disponibles

### Materiales Opacos
- `matte_red`: Rojo mate con poca reflexión
- `glossy_blue`: Azul con acabado semi-brillante

### Materiales Reflectivos
- `polished_gold`: Oro pulido con alta reflexión
- `lacquer_red`: Rojo laqueado con reflexión media

### Materiales Transparentes
- `clear_glass`: Vidrio transparente (IOR: 1.50)
- `green_glass`: Vidrio con tinte verde (IOR: 1.52)

## Ejemplos de Uso

### Crear una Esfera de Vidrio
```python
glass_sphere = Sphere(
    position=[0, 0, -5],
    radius=1,
    material=clear_glass
)
rend.scene.append(glass_sphere)
```

### Configurar Environment Map
```python
rend.envMap = BMPTexture('tu_textura.bmp')
```

### Ajustar Calidad de Renderizado
```python
# En gl.py, modificar la profundidad de recursión
self.maxRecursionDepth = 5  # Más reflexiones = mejor calidad
```

## Salida

El programa genera dos tipos de salida:
1. **Vista en tiempo real**: Ventana de Pygame para visualización interactiva
2. **Imagen final**: Archivo `output.bmp` con el renderizado completo

## Rendimiento

### Optimizaciones Implementadas
- Cálculo eficiente de intersecciones
- Limitación de profundidad de recursión
- Optimización de operaciones vectoriales con NumPy

### Tiempos de Renderizado
- **720x720 px**: ~30-60 segundos (dependiendo de la complejidad)
- **Factores que afectan el rendimiento**:
  - Número de objetos en la escena
  - Cantidad de luces
  - Profundidad de recursión
  - Materiales transparentes/reflectivos

## Controles

- **ESC**: Salir del programa
- La ventana se actualiza en tiempo real durante el renderizado

## Limitaciones Conocidas

- Solo soporta geometría esférica y planos
- Texturas limitadas a formato BMP
- No incluye aceleración por estructuras espaciales (KD-tree, BVH)
- Renderizado single-threaded

## Desarrollo Futuro

### Características Planeadas
- [ ] Soporte para más formatos de imagen
- [ ] Implementación de más primitivas geométricas
- [ ] Aceleración mediante GPU
- [ ] Importación de modelos 3D
- [ ] Sistema de partículas
- [ ] Volumetric lighting

## Créditos

Proyecto desarrollado como parte del curso de Gráficas por Computadora.

### Tecnologías Utilizadas
- **Python**: Lenguaje principal
- **Pygame**: Manejo de ventanas y eventos
- **NumPy**: Operaciones matemáticas vectoriales

## Licencia

Este proyecto es de uso educativo y está disponible bajo licencia MIT.
