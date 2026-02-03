import struct

def GenerateBMP(filename: str, width: int, height: int, byteDepth: int,
                colorBuffer: list[list[tuple]]) -> None:
    """
    Escribe un BMP 24 bpp (byteDepth=3) o 32 bpp (byteDepth=4) desde colorBuffer[y][x].
    colorBuffer puede traer canales en 0..255 (int) o 0..1 (float).
    """
    assert byteDepth in (3, 4), "Solo 24 o 32 bpp"
    # Validar forma del buffer (opcional pero útil):
    assert len(colorBuffer) == height and len(colorBuffer[0]) == width, \
        f"shape mismatch: got {len(colorBuffer)}x{len(colorBuffer[0])}, expected {height}x{width}"

    row_bytes  = width * byteDepth
    row_stride = (row_bytes + 3) & ~3   # múltiplo de 4
    pad_len    = row_stride - row_bytes
    padding    = b'\x00' * pad_len
    image_size = row_stride * height
    file_size  = 14 + 40 + image_size

    with open(filename, "wb") as f:
        # --- BITMAPFILEHEADER (14 bytes) ---
        f.write(b"BM")
        f.write(struct.pack("<I", file_size))     # bfSize
        f.write(b"\x00\x00\x00\x00")              # bfReserved1+2
        f.write(struct.pack("<I", 14 + 40))       # bfOffBits = 54

        # --- BITMAPINFOHEADER (40 bytes) ---
        f.write(struct.pack("<I", 40))            # biSize
        f.write(struct.pack("<i", width))         # biWidth  (signed)
        f.write(struct.pack("<i", height))        # biHeight (signed, positivo => bottom-up)
        f.write(struct.pack("<H", 1))             # biPlanes
        f.write(struct.pack("<H", byteDepth * 8)) # biBitCount
        f.write(struct.pack("<I", 0))             # biCompression = BI_RGB
        f.write(struct.pack("<I", image_size))    # biSizeImage
        f.write(struct.pack("<i", 2835))          # biXPelsPerMeter (~72 dpi)
        f.write(struct.pack("<i", 2835))          # biYPelsPerMeter
        f.write(struct.pack("<I", 0))             # biClrUsed
        f.write(struct.pack("<I", 0))             # biClrImportant

        # --- Pixel data (bottom-up) ---
        for y in range(height - 1, -1, -1):
            row = colorBuffer[y]                  # lista de (r,g,b) o (r,g,b,a)
            buf = bytearray(row_bytes)
            i = 0
            if byteDepth == 3:
                for (r, g, b) in row:
                    # Soporta floats 0..1 o ints 0..255
                    if isinstance(r, float):
                        r = int(r * 255 + 0.5); g = int(g * 255 + 0.5); b = int(b * 255 + 0.5)
                    # Clamp
                    if r < 0: r = 0
                    elif r > 255: r = 255
                    if g < 0: g = 0
                    elif g > 255: g = 255
                    if b < 0: b = 0
                    elif b > 255: b = 255
                    # BMP = B, G, R
                    buf[i] = b; buf[i+1] = g; buf[i+2] = r
                    i += 3
            else:  # 32 bpp BGRA
                for px in row:
                    if len(px) == 3:
                        r, g, b = px; a = 255
                    else:
                        r, g, b, a = px
                    if isinstance(r, float):
                        r = int(r * 255 + 0.5); g = int(g * 255 + 0.5)
                        b = int(b * 255 + 0.5); a = int(a * 255 + 0.5)
                    r = 0 if r < 0 else 255 if r > 255 else r
                    g = 0 if g < 0 else 255 if g > 255 else g
                    b = 0 if b < 0 else 255 if b > 255 else b
                    a = 0 if a < 0 else 255 if a > 255 else a
                    buf[i] = b; buf[i+1] = g; buf[i+2] = r; buf[i+3] = a
                    i += 4
            f.write(buf)
            if pad_len:
                f.write(padding)
