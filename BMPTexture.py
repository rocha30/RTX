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
        if 0 <= u <= 1 and 0 <= v <= 1:
            x = int(u * (self.width  - 1))
            y = int((1.0 - v) * (self.height - 1))  # <- flip vertical
            return self.pixels[y][x]
        return None

