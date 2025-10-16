# RTX - Python Ray Tracer

Un motor de ray tracing implementado en Python usando Pygame, capaz de renderizar escenas 3D con geometrías primitivas, iluminación realista, reflexiones, refracciones, diferentes tipos de materiales y **texturas BMP de alta calidad**.

![Render del Proyecto 2 con Texturas](RenderProyecto2.png)
![Imagen de Referencia](Proyecto2.png)

## 🆕 Proyecto 2: Sistema de Texturas BMP Implementado

### Nuevas Características de Texturizado
- **✅ Texturas BMP completas**: Implementación robusta para cargar y aplicar texturas .bmp
- **✅ Coordenadas UV automáticas**: Cálculo inteligente de coordenadas de textura para todas las geometrías
- **✅ Mapeo de texturas realista**: Arena, madera y environment mapping
- **✅ Repetición de texturas**: Sistema de tiling para texturas que se repiten naturalmente
- **✅ Manejo robusto de errores**: Conversión segura de tipos y manejo de casos extremos

### Archivos de Textura Incluidos
- `sand.bmp` - Textura de arena para el suelo del jardín zen
- `wood.bmp` - Textura de madera para pedestales y mobiliario  
- `Fondo.bmp` - Environment map para reflexiones de montañas

### Geometrías con Soporte de Texturas
- **Plane**: Coordenadas UV calculadas con repetición configurable (cada 4 unidades)
- **AABB**: Coordenadas UV por cara con mapeo apropiado según la superficie
- **Sphere**: Coordenadas esféricas UV para environment mapping
- **Otros**: Sistema extensible para agregar texturas a cualquier geometría

## Características Implementadas

### 🎯 Geometrías Avanzadas (Lab 8)
- **Cilindros**: Cilindros 3D completos con tapas y orientación configurable
- **Toros**: Formas toroidales (donut) usando ecuaciones cuárticas paramétricas
- **Planos**: Planos infinitos para construir paredes, pisos y techos
- **Cubos (AABB)**: Cubos alineados a los ejes (implementación previa)
- **Esferas**: Esferas con coordenadas de textura esféricas (implementación previa)
- **Triángulos**: Triángulos 3D con algoritmo Möller–Trumbore (implementación previa)
- **Discos**: Círculos 3D con posición, normal y radio configurables (implementación previa)

### 🎨 Materiales Avanzados
- **Materiales Opacos**: Superficies mate con diferentes colores y especularidad
- **Materiales Reflectivos**: Metales pulidos con reflexiones especulares
- **Materiales Transparentes**: Vidrio con refracción y diferentes índices
- **Materiales Optimizados**: Versiones más rápidas para mejor rendimiento

### 💡 Sistema de Iluminación Completo
- **Luz Ambiental**: Iluminación global uniforme
- **Luz Direccional**: Simulación de luz solar con sombras direccionales  
- **Luz Puntual**: Fuentes de luz con atenuación por distancia
- **Luz Spot**: Focos direccionales con ángulos internos y externos
- **Modelo de Phong**: Cálculo completo de iluminación difusa y especular

### 🌍 Efectos Visuales
- **Environment Mapping**: Reflexiones del entorno usando texturas BMP
- **Sombras Proyectadas**: Ray tracing para sombras realistas
- **Reflexiones Recursivas**: Múltiples rebotes para materiales reflectivos
- **Refracción Física**: Implementación de la Ley de Snell y efecto Fresnel

### 🎨 Sistema de Texturas BMP (Proyecto 2)
- **Carga de Texturas BMP**: Parser robusto que maneja formatos de 24 bits
- **Coordenadas UV Automáticas**: Cálculo inteligente para cada tipo de geometría
- **Mapeo por Cara**: AABB calcula UV diferentes según la superficie intersectada
- **Repetición de Texturas**: Sistema de tiling configurable para patrones repetitivos
- **Manejo de Bordes**: Clamp seguro y wrapping para coordenadas fuera de [0,1]
- **Conversión de Tipos**: Manejo robusto de arrays numpy para evitar errores de dispatch

## Estructura del Proyecto

```
RTX/
├── RayTracer.py              # Escena principal del Lab 8 (Cylinder + Torus)
├── gl.py                     # Motor de renderizado y ray casting
├── figures.py                # Geometrías: Cylinder, Torus, Sphere, Plane, Triangle, Disk, AABB, OBB
├── Material.py               # Materiales y cálculo de superficie
├── lights.py                 # Sistema completo de iluminación
├── intercept.py              # Estructura de datos de intersección
├── Camera.py                 # Sistema de cámara y proyección
├── MathLib.py                # Funciones matemáticas auxiliares
├── refractionFunctions.py    # Cálculos ópticos avanzados
├── BMPTexture.py             # Carga y manejo de texturas
├── BMP_Writer.py             # Exportación de imágenes BMP
├── Fondo.bmp                 # Texture de environment map
├── test_intersections.py     # Pruebas unitarias para intersecciones
└── output.bmp                # Resultado del Laboratorio 8
```

## Instalación

### Requisitos
- Python 3.8+
- Pygame 2.0+
- NumPy

### Instalación de dependencias
```bash
# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install pygame numpy
```

## Uso

### Ejecución del Proyecto 2 con Texturas
```bash
python RayTracer.py
```

Este comando renderiza la escena del Proyecto 2 que incluye:
- **Jardín zen texturizado** con arena real usando `sand.bmp`
- **Pedestales de madera** con textura natural usando `wood.bmp`
- **Environment mapping** con fondo de montañas usando `Fondo.bmp`
- **3 Esferas zen** con materiales oscuros mate para contraste
- **Iluminación múltiple** optimizada para mostrar detalles de texturas

### Ejecución del Laboratorio 8
```bash
python RayTracer.py
```

Este comando renderiza la escena del Lab 8 que incluye:
- **Un cuarto cerrado** con 5 planos (piso, techo, 3 paredes) con colores contrastantes
- **3 Cilindros** con diferentes orientaciones, tamaños y materiales:
  - Cilindro vertical opaco rojo (pequeño)
  - Cilindro diagonal reflectivo dorado (mediano) 
  - Cilindro horizontal transparente azul (grande)
- **3 Toros** con diferentes tamaños y materiales:
  - Toro opaco azul brillante (pequeño)
  - Toro reflectivo rojo (mediano)
  - Toro reflectivo metálico (grande)
- **Sistema de iluminación mejorado** con 5 luces para mejor visibilidad

### Personalización de Escena

Puedes modificar la escena editando `RayTracer.py`:

```python
# Configuración de resolución (menor = más rápido, mayor = mejor calidad de texturas)
width = 720
height = 720  # Resolución recomendada para texturas nítidas

# Agregar superficie con textura de arena
sand_material = Material(
    diffuse=[0.8, 0.75, 0.6],
    spec=4,
    ks=0.0,
    texture=BMPTexture('sand.bmp'),
    matType=OPAQUE
)
rend.scene.append(Plane(position=[0, -4, 0], normal=[0, 1, 0], material=sand_material))

# Agregar objeto con textura de madera
wood_material = Material(
    diffuse=[0.6, 0.4, 0.2],
    spec=0.2,
    ks=0.1,
    texture=BMPTexture('wood.bmp'),
    matType=OPAQUE
)
rend.scene.append(AABB(min_point=[-1, -2, -3], max_point=[1, -1, -2], material=wood_material))

# Environment map para reflexiones
rend.envMap = BMPTexture('Fondo.bmp')
```

### Personalización Anterior (Lab 8)

También puedes usar la configuración del Lab 8 sin texturas:

```python
# Configuración de resolución (menor = más rápido)
width = 800
height = 600

# Agregar un Cilindro
rend.scene.append(Cylinder(
    position=[-2.5, -1, -5], 
    axis=[0, 1, 0],           # Eje Y (vertical)
    radius=0.4, 
    height=1.2, 
    material=Material(diffuse=[0.9, 0.2, 0.2], spec=32, ks=0.0, matType=OPAQUE)
))

# Agregar un Toro
rend.scene.append(Torus(
    position=[2, -1.8, -4.5], 
    major_radius=0.6,         # Radio mayor (centro a tubo)
    minor_radius=0.25,        # Radio menor (grosor del tubo)
    material=Material(diffuse=[0.2, 0.3, 0.9], spec=32, ks=0.0, matType=OPAQUE)
))

# Configurar iluminación optimizada
rend.lights.append(AmbientLight(intensity=0.6))
rend.lights.append(DirectionalLight(direction=[0, -1, -1], intensity=0.8))
rend.lights.append(PointLight(position=[-2, 2, -3], intensity=0.7))
```
```

## Materiales Disponibles

### Materiales Opacos
- `matte_red`: Superficie roja mate
- `glossy_blue`: Azul con acabado brillante  
- `soft_white`: Blanco suave para paredes
- `warm_gray`: Gris cálido para pisos
- `light_beige`: Beige claro para superficies neutras
- `pale_blue`: Azul pálido suave

### Materiales Reflectivos  
- `polished_gold`: Oro altamente reflectivo
- `soft_gold`: Oro con reflexiones suaves (más rápido)
- `lacquer_red`: Rojo con acabado lacado

### Materiales Transparentes
- `clear_glass`: Vidrio transparente sin tinte
- `green_glass`: Vidrio con tinte verdoso

### Materiales Reflectivos
- `polished_gold`: Oro pulido con alta reflexión
- `lacquer_red`: Rojo laqueado con reflexión media

### Materiales Transparentes
- `clear_glass`: Vidrio transparente (IOR: 1.50)
## Proyecto 2: Implementación Técnica de Texturas

### Mejoras Implementadas

#### 1. BMPTexture.py - Carga Robusta de Texturas
```python
class BMPTexture:
    def getColor(self, u, v):
        # Wrapping automático para repetición de texturas
        u = u - int(u) if u >= 0 else 1 + (u - int(u))
        v = v - int(v) if v >= 0 else 1 + (v - int(v))
        
        # Clamp seguro dentro de límites
        u = max(0.0, min(1.0, u))
        v = max(0.0, min(1.0, v))
        
        # Conversión segura de índices
        x = max(0, min(self.width - 1, int(u * (self.width - 1))))
        y = max(0, min(self.height - 1, int((1.0 - v) * (self.height - 1))))
        
        return self.pixels[y][x]
```

#### 2. figures.py - Coordenadas UV para Geometrías

**Plane (Suelo texturizado):**
```python
def ray_intersect(self, orig, dir):
    # ... cálculo de intersección ...
    
    # Coordenadas UV con repetición cada 4 unidades
    if abs(self.normal[1]) > 0.9:  # Plano horizontal
        u = float(P[0] % 4.0) / 4.0  # Repetir en X
        v = float(P[2] % 4.0) / 4.0  # Repetir en Z
    else:  # Plano vertical
        u = float(P[0] % 4.0) / 4.0
        v = float(P[1] % 4.0) / 4.0
    
    return Intercept(point=P, normal=self.normal, distance=t, 
                    rayDirection=dir, obj=self, texCoords=[u, v])
```

**AABB (Cubos con textura por cara):**
```python
def ray_intersect(self, orig, dir):
    # ... cálculo de intersección ...
    
    # UV diferentes según la cara intersectada
    if abs(normal[0]) > 0.5:  # Cara lateral (X)
        u = float((P[2] - self.min_point[2]) / (self.max_point[2] - self.min_point[2]))
        v = float((P[1] - self.min_point[1]) / (self.max_point[1] - self.min_point[1]))
    elif abs(normal[1]) > 0.5:  # Cara superior/inferior (Y)
        u = float((P[0] - self.min_point[0]) / (self.max_point[0] - self.min_point[0]))
        v = float((P[2] - self.min_point[2]) / (self.max_point[2] - self.min_point[2]))
    else:  # Cara frontal/trasera (Z)
        u = float((P[0] - self.min_point[0]) / (self.max_point[0] - self.min_point[0]))
        v = float((P[1] - self.min_point[1]) / (self.max_point[1] - self.min_point[1]))
    
    # Clamp manual para evitar errores de numpy
    u = max(0.0, min(1.0, u)) if abs(self.max_point[0] - self.min_point[0]) > 1e-6 else 0.0
    v = max(0.0, min(1.0, v)) if abs(self.max_point[1] - self.min_point[1]) > 1e-6 else 0.0
    
    return Intercept(point=P, normal=normal, distance=t,
                    rayDirection=dir, obj=self, texCoords=[u, v])
```

#### 3. Material.py - Aplicación de Texturas
```python
def GetSurfaceColor(self, intercept, renderer, recursion=0):
    # ... iluminación base ...
    
    # Aplicar textura si está disponible
    if self.texture and intercept.texCoords:
        textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
        if textureColor:  # Verificación de color válido
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]
    
    # ... resto del cálculo de iluminación ...
```

### Problemas Resueltos

#### Error de Tipos numpy
**Problema:** `TypeError: 'float' object cannot be interpreted as an integer`
**Solución:** Conversión explícita a `float()` antes de operaciones matemáticas

#### División por Cero
**Problema:** Coordenadas UV indefinidas en caras muy pequeñas
**Solución:** Verificación de épsilon antes de división: `abs(denominator) > 1e-6`

#### Coordenadas Fuera de Rango
**Problema:** UV coordinates fuera de [0,1] causando errores
**Solución:** Clamp manual y wrapping automático para repetición

#### Texturas No Aparecían
**Problema:** `texCoords=None` en geometrías
**Solución:** Implementación de cálculo UV para `Plane` y `AABB`

### Arquitectura de Texturas

```
Texture Pipeline:
BMPTexture.py -> Material.py -> figures.py -> gl.py
     ↓              ↓             ↓           ↓
  Load BMP → Apply to Material → Calculate UV → Render Pixel
```

## Laboratorio 8: Figuras Geométricas Avanzadas

### Objetivo Cumplido ✅
Implementación de 2 nuevas figuras geométricas no vistas en clase:
- ✅ **3 Cilindros**: Con diferentes orientaciones (vertical, diagonal, horizontal) y materiales (opaco, reflectivo, transparente)
- ✅ **3 Toros**: Con diferentes tamaños y materiales (opaco, reflectivo, reflectivo metálico)
- ✅ **Cuarto cerrado**: 5 planos con colores optimizados para contraste
- ✅ **Sin texturas compartidas**: Cumpliendo requisitos de originalidad

### Características Técnicas Lab 8
- **Ray-Cylinder Intersection**: Intersección con superficie lateral y tapas circulares
- **Ray-Torus Intersection**: Resolución de ecuaciones cuárticas paramétricas con optimización de esfera envolvente
- **Materiales Diversos**: Opacos, reflectivos y transparentes según rúbrica
- **Algoritmos Robustos**: Manejo de casos especiales y épsilon para estabilidad numérica
- **Optimización de Rendimiento**: Early-out con esferas envolventes y verificaciones matemáticas

### Implementación Matemática
- **Cilindro**: Intersección analítica con superficie cuadrática + verificación de tapas
- **Toro**: Ecuación cuártica `(√(x²+z²) - R)² + y² = r²` con resolución de polinomios
- **Normales Correctas**: Gradientes calculados analíticamente para cada superficie
- **Estabilidad Numérica**: Conversiones explícitas para evitar errores de dispatch de NumPy

## Ejemplos de Uso

### Crear un Cilindro
```python
cylinder = Cylinder(
    position=[-2, 0.5, -7],    # Centro del cilindro
    axis=[0.3, 1, 0.2],        # Vector de dirección (se normaliza automáticamente)
    radius=0.5,                # Radio del cilindro
    height=1.5,                # Altura total
    material=Material(diffuse=[0.8, 0.6, 0.1], spec=64, ks=0.8, matType=REFLECTIVE)
)
rend.scene.append(cylinder)
```

### Crear un Toro
```python
torus = Torus(
    position=[2.5, 0, -6],     # Centro del toro
    major_radius=0.8,          # Radio mayor (centro a tubo)
    minor_radius=0.3,          # Radio menor (grosor del tubo)
    material=Material(diffuse=[0.8, 0.1, 0.1], spec=96, ks=0.7, matType=REFLECTIVE)
)
rend.scene.append(torus)
```

### Crear un Cubo (AABB) - Implementación Previa
```python
cube = AABB(
    min_point=[-1, -1, -1],  # Esquina mínima
    max_point=[1, 1, 1],     # Esquina máxima  
    material=soft_gold
)
rend.scene.append(cube)
```

### Configurar Iluminación Lab 8
```python
# Configuración optimizada para Lab 8
rend.lights.append(AmbientLight(intensity=0.6))  # Más luz ambiental
rend.lights.append(DirectionalLight(direction=[0, -1, -1], intensity=0.8))
rend.lights.append(PointLight(position=[-2, 2, -3], intensity=0.7))  # Luz desde arriba-izquierda  
rend.lights.append(PointLight(position=[2, 1, -4], intensity=0.6))   # Luz desde derecha
rend.lights.append(PointLight(position=[0, -1, -2], intensity=0.5))  # Luz frontal baja
```

## Pruebas y Validación

### Test de Intersecciones
```bash
python test_intersections.py
```

Resultado esperado:
```
Testing OBB and Torus intersections
obb_center hit= True
  point [-0. -0. -4.] normal [0. 0. 1.] dist 4.0
obb_miss hit= False
torus_hit hit= True
  point [2.5 0.  -3.5] normal [0. 0. 1.] dist 3.5
torus_miss hit= False
```

## Salida

El programa genera dos tipos de salida:
1. **Vista en tiempo real**: Ventana de Pygame para visualización interactiva
2. **Imagen final**: Archivo `output.bmp` con el renderizado completo en alta calidad

## Rendimiento

### Configuraciones Recomendadas para Texturas (Proyecto 2)
```python
# Desarrollo rápido con texturas (30-60 segundos)
width, height = 512, 512
maxRecursionDepth = 2
# Texturas visibles pero render rápido

# Calidad media con texturas nítidas (1-2 minutos)
width, height = 720, 720  # ⭐ RECOMENDADO para texturas
maxRecursionDepth = 2
# Balance perfecto: texturas nítidas y tiempo razonable

# Render de alta calidad (3-5 minutos)  
width, height = 1024, 1024
maxRecursionDepth = 3
# Máxima calidad de texturas para presentaciones
```

### Configuraciones Lab 8 (Sin texturas)
```python
# Desarrollo rápido (Lab 8 - 10-30 segundos)
width, height = 400, 300
maxRecursionDepth = 2
# Iluminación optimizada con 5 luces

# Render de producción (Lab 8 - 60-120 segundos)  
width, height = 800, 600
maxRecursionDepth = 3
# Iluminación completa + materiales reflectivos y transparentes
```

### Factores de Rendimiento Lab 8
- **Geometría Compleja**: Toros requieren resolución de ecuaciones cuárticas
- **Cilindros**: Intersección con superficie + tapas (múltiples cálculos por rayo)
- **Materiales reflectivos**: Múltiples toros y cilindros reflectivos generan rayos adicionales
- **Optimizaciones**: Esfera envolvente para Torus reduce cálculos innecesarios
- **Profundidad de recursión**: Control de rebotes de reflexión/refracción

### Optimizaciones Aplicadas Lab 8
- Bounding sphere early-out para intersección de Toros
- Conversión explícita de tipos para evitar errores de NumPy dispatch
- Verificación de épsilon para evitar división por cero
- Cálculo analítico de normales usando gradientes
- Manejo robusto de raíces cuárticas complejas
- Early termination en ray casting para geometrías complejas

## Desarrollo

### Arquitectura del Sistema
- **Modular**: Cada componente en archivo separado
- **Extensible**: Fácil agregar nuevas geometrías y materiales
- **Mantenible**: Código documentado y estructurado

### Próximas Características Planeadas
- Implementación de más figuras cuárticas (elipsoides, hiperboloides)
- Anti-aliasing mejorado para geometrías complejas
- Aceleración con BVH (Bounding Volume Hierarchy) para escenas complejas
- Soporte para mallas triangulares importadas
- Efectos volumétricos y subsurface scattering
- Optimización GPU con compute shaders

---

## Evidencia de Desarrollo con IA

### Proceso de Implementación Documentado
Este proyecto del Lab 8 fue desarrollado con asistencia de IA (GitHub Copilot), cumpliendo con los requisitos de documentar la conversación. El proceso incluyó:

1. **Análisis de rúbrica**: Revisión de requisitos del Lab 8
2. **Selección de figuras**: Elección de Torus y Cylinder como figuras no vistas en clase
3. **Implementación matemática**: Desarrollo de algoritmos de intersección ray-surface
4. **Debugging y optimización**: Resolución de errores de NumPy y mejoras de rendimiento
5. **Testing**: Creación de pruebas unitarias para validar intersecciones
6. **Composición de escena**: Configuración final con 3 instancias de cada figura

### Figuras Implementadas con IA
- **Torus**: Ecuación cuártica paramétrica con resolución de polinomios
- **Cylinder**: Intersección con superficie cuadrática y tapas circulares
- **OBB**: Bounding box orientado (implementación adicional)
- **TruncatedSphere**: Esfera truncada (experimentación intermedia)

### Challenges Resueltos
- Manejo de errores de dispatch de NumPy con tipos mixtos
- Cálculo correcto de normales para superficies paramétricas
- Optimización de rendimiento para ecuaciones cuárticas
- Debugging de intersecciones complejas con ray tracing

---

## Créditos

**Autor**: Mario Rocha  
**Curso**: Gráficos por Computadora  
**Proyectos**: 
- Lab 8 - Figuras Geométricas Avanzadas
- **Proyecto 2 - Sistema de Texturas BMP**  
**Fecha**: Octubre 2025  
**Desarrollo con IA**: GitHub Copilot (conversación documentada)

**Tecnologías utilizadas**:
- Python 3.13
- Pygame 2.6.1  
- NumPy para operaciones vectoriales y resolución de polinomios
- **Texturas BMP**: Parser personalizado para formatos de 24 bits
- Matemáticas avanzadas: ecuaciones cuárticas, intersección ray-surface, gradientes analíticos, coordenadas UV
## Limitaciones Conocidas

- Resolución de ecuaciones cuárticas puede ser computacionalmente intensiva
- Texturas limitadas a formato BMP (no utilizadas en Lab 8 por requisitos)
- No incluye aceleración por estructuras espaciales (KD-tree, BVH)
- Renderizado single-threaded (puede tardar 1-2 minutos en alta resolución)
- Algunas configuraciones de Torus pueden producir artefactos numéricos en casos extremos

## Desarrollo Futuro

### Características Planeadas Lab 9+
- [ ] Soporte para más formatos de imagen (PNG, JPEG)
- [ ] Implementación de más primitivas geométricas (elipsoides, paraboloides)
- [ ] Aceleración mediante GPU con compute shaders
- [ ] Importación de modelos 3D (.obj, .stl)
- [ ] Sistema de partículas y efectos volumétricos
- [ ] Volumetric lighting y atmospheric effects

## Controles

- **ESC**: Salir del programa
- La ventana se actualiza en tiempo real durante el renderizado
- Se genera automáticamente `output.bmp` al finalizar el render

## Créditos

Proyecto desarrollado como parte del curso de Gráficas por Computadora.

### Tecnologías Utilizadas
- **Python**: Lenguaje principal
- **Pygame**: Manejo de ventanas y eventos
- **NumPy**: Operaciones matemáticas vectoriales

## Licencia

Este proyecto es de uso educativo y está disponible bajo licencia MIT.

---

## Anexo: Colaboración con IA

### Documentación del Proceso de Desarrollo
Como parte de los requisitos del Lab 8, se documenta el uso de IA (GitHub Copilot) en el desarrollo de este proyecto:

**Figuras implementadas con asistencia de IA:**
- `Cylinder`: Algoritmo de intersección ray-cylinder con tapas
- `Torus`: Resolución de ecuaciones cuárticas para formas toroidales  
- `OBB`: Oriented Bounding Box (implementación adicional)

**Problemas resueltos colaborativamente:**
1. Errores de dispatch de NumPy con tipos mixtos
2. Cálculo correcto de normales para superficies paramétricas  
3. Optimización de rendimiento con early-out algorithms
4. Debug de intersecciones complejas

**Conversación completa disponible** según requisitos de la rúbrica.

### Resultado Final
✅ **2 figuras nuevas implementadas** (Cylinder, Torus)  
✅ **3 instancias de cada una** con materiales opaco/reflectivo/transparente  
✅ **Sin uso de texturas compartidas en clase**  
✅ **Documentación completa del proceso con IA**