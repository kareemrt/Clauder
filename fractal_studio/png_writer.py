"""Minimal pure-Python PNG writer using only stdlib (struct + zlib)."""
import struct
import zlib
from typing import List, Tuple


def write_png(filepath: str, pixels: List[Tuple[int, int, int]],
              width: int, height: int) -> None:
    """Write a list of (r, g, b) pixels as a 24-bit PNG file."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        payload = tag + data
        return (
            struct.pack(">I", len(data))
            + payload
            + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF)
        )

    # Raw scanline data: each row preceded by filter-type byte 0 (None)
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            r, g, b = pixels[y * width + x]
            raw.append(r)
            raw.append(g)
            raw.append(b)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    iend = chunk(b"IEND", b"")

    with open(filepath, "wb") as f:
        f.write(signature + ihdr + idat + iend)
