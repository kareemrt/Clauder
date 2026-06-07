"""A minimal PNG encoder built only on top of `zlib` and `struct`.

PNG is a deceptively simple format once you strip away the optional
features: a signature, a handful of length-prefixed/CRC-checked chunks,
and a zlib-compressed grid of scanlines (each prefixed with a filter
byte). Implementing it directly avoids pulling in Pillow/numpy just to
dump an RGB grid to disk.
"""

from __future__ import annotations

import struct
import zlib

_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(tag: bytes, data: bytes) -> bytes:
    body = tag + data
    crc = zlib.crc32(body) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + body + struct.pack(">I", crc)


def write_png(path: str, pixels: list[list[tuple[int, int, int]]]) -> None:
    """Write an RGB grid (rows of (r, g, b) tuples) to `path` as a PNG."""
    height = len(pixels)
    width = len(pixels[0]) if height else 0

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)

    # Filter type 0 ("None") prefixes every scanline; the row bytes follow.
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for r, g, b in row:
            raw += bytes((r, g, b))

    idat = zlib.compress(bytes(raw), level=9)

    with open(path, "wb") as fh:
        fh.write(_SIGNATURE)
        fh.write(_chunk(b"IHDR", ihdr))
        fh.write(_chunk(b"IDAT", idat))
        fh.write(_chunk(b"IEND", b""))
