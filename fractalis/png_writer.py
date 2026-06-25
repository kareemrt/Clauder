"""Minimal PNG encoder using only the standard library (zlib + struct).

Supports 8-bit RGB, non-interlaced, filter-type-0 (None) scanlines.
This is enough to write any RGB pixel buffer fractalis produces without
pulling in Pillow or numpy.
"""

import struct
import zlib

_SIGNATURE = bytes([137, 80, 78, 71, 13, 10, 26, 10])


def _chunk(chunk_type, data):
    header = struct.pack(">I", len(data)) + chunk_type
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return header + data + struct.pack(">I", crc)


def write_png(path, width, height, pixels):
    """Write an RGB image to ``path``.

    ``pixels`` must be a flat bytes-like object of length
    ``width * height * 3``, row-major, top row first.
    """
    expected = width * height * 3
    if len(pixels) != expected:
        raise ValueError(f"expected {expected} bytes of pixel data, got {len(pixels)}")

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)

    raw = bytearray()
    stride = width * 3
    for row in range(height):
        raw.append(0)  # filter type: None
        raw.extend(pixels[row * stride:(row + 1) * stride])
    idat = zlib.compress(bytes(raw), level=9)

    with open(path, "wb") as f:
        f.write(_SIGNATURE)
        f.write(_chunk(b"IHDR", ihdr))
        f.write(_chunk(b"IDAT", idat))
        f.write(_chunk(b"IEND", b""))
