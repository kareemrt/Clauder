import os
import struct
import tempfile
import unittest
import zlib

from fractalis.png_writer import write_png

PNG_SIGNATURE = bytes([137, 80, 78, 71, 13, 10, 26, 10])


class PngWriterTest(unittest.TestCase):
    def test_writes_valid_signature_and_ihdr(self):
        width, height = 4, 3
        pixels = bytes([0, 0, 0]) * (width * height)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.png")
            write_png(path, width, height, pixels)
            with open(path, "rb") as f:
                data = f.read()

        self.assertEqual(data[:8], PNG_SIGNATURE)

        ihdr_len = struct.unpack(">I", data[8:12])[0]
        self.assertEqual(ihdr_len, 13)
        self.assertEqual(data[12:16], b"IHDR")
        w, h, depth, color_type = struct.unpack(">IIBB", data[16:26])
        self.assertEqual((w, h, depth, color_type), (width, height, 8, 2))

        self.assertIn(b"IDAT", data)
        self.assertIn(b"IEND", data)

    def test_roundtrips_pixel_data_through_zlib(self):
        width, height = 2, 2
        pixels = bytes([255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255])
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.png")
            write_png(path, width, height, pixels)
            with open(path, "rb") as f:
                data = f.read()

        # Locate the IDAT chunk and decompress it manually to confirm the
        # filtered scanlines match the input pixels.
        idx = data.index(b"IDAT")
        length = struct.unpack(">I", data[idx - 4:idx])[0]
        idat = data[idx + 4: idx + 4 + length]
        raw = zlib.decompress(idat)

        stride = width * 3
        rows = [raw[i * (stride + 1) + 1: i * (stride + 1) + 1 + stride] for i in range(height)]
        self.assertEqual(b"".join(rows), pixels)

    def test_rejects_wrong_length_pixel_buffer(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.png")
            with self.assertRaises(ValueError):
                write_png(path, 2, 2, bytes([0, 0, 0]))


if __name__ == "__main__":
    unittest.main()
