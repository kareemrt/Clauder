import numpy as np
import pytest

from fracta.palette import apply_palette, available_palettes, get_palette_lut


def test_available_palettes_nonempty():
    assert "ocean" in available_palettes()


def test_get_palette_lut_shape():
    lut = get_palette_lut("fire", size=256)
    assert lut.shape == (256, 3)
    assert lut.dtype == np.uint8


def test_apply_palette_maps_0_and_1_to_endpoints():
    values = np.array([[0.0, 1.0]])
    img = apply_palette(values, "mono")
    assert tuple(img[0, 0]) == (0, 0, 0)
    assert tuple(img[0, 1]) == (255, 255, 255)


def test_unknown_palette_raises():
    with pytest.raises(ValueError):
        get_palette_lut("not-a-palette")
