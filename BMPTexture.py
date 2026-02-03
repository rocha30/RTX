import struct

class BMPTexture(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            # Offset al inicio de los datos de pixeles (byte 10, 4 bytes little-endian)
            f.seek(10)
            data_offset = struct.unpack('<I', f.read(4))[0]

            # Ancho y alto (bytes 18 y 22, 4 bytes cada uno, little-endian con signo)
            f.seek(18)
            self.width  = struct.unpack('<i', f.read(4))[0]
            height_raw  = struct.unpack('<i', f.read(4))[0]

            # Si height es positivo -> bitmap bottom-up; si es negativo -> top-down
            bottom_up = height_raw > 0
            self.height = abs(height_raw)

            # Ir al inicio de los datos de imagen
            f.seek(data_offset)

            # BMP de 24bpp: 3 bytes por pixel (B, G, R), padding por fila a múltiplo de 4 bytes
            row_bytes_no_pad = self.width * 3
            row_stride = (row_bytes_no_pad + 3) & ~3   # redondear a múltiplo de 4
            padding = row_stride - row_bytes_no_pad

            self.pixels = []  # pixels[y][x] = [r, g, b] en floats 0..1

            # Leer filas en el orden del archivo
            for _ in range(self.height):
                row = []
                for _ in range(self.width):
                    b = f.read(1)[0] / 255.0
                    g = f.read(1)[0] / 255.0
                    r = f.read(1)[0] / 255.0
                    row.append([r, g, b])
                # Saltar padding
                if padding:
                    f.read(padding)
                self.pixels.append(row)

            # Si es bottom-up, la primera fila leída es la inferior -> invertir para tener y=0 arriba
            if bottom_up:
                self.pixels.reverse()

    def getColor(self, u, v):
        # Asegurar que u y v estén en el rango [0,1] usando módulo para repetir la textura
        u = u - int(u) if u >= 0 else 1 + (u - int(u))
        v = v - int(v) if v >= 0 else 1 + (v - int(v))
        
        # Asegurar que estén exactamente en [0,1]
        u = max(0.0, min(1.0, u))
        v = max(0.0, min(1.0, v))
        
        x = int(u * (self.width  - 1))
        y = int((1.0 - v) * (self.height - 1))  # <- flip vertical
        
        # Asegurar que los índices estén dentro de los límites
        x = max(0, min(self.width - 1, x))
        y = max(0, min(self.height - 1, y))
        
        return self.pixels[y][x]

