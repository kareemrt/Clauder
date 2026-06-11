import numpy as np
import pytest

from fractalforge.palettes import apply_palette, available_palettes


def test_available_palettes_nonempty():
    names = available_palettes()
    assert "fire" in names
    assert len(names) >= 4


@pytest.mark.parametrize("name", available_palettes())
def test_apply_palette_produces_valid_rgb(name):
    values = np.linspace(0, 1, 10).reshape(2, 5)
    rgb = apply_palette(values, name)
    assert rgb.shape == (2, 5, 3)
    assert rgb.dtype == np.uint8
    assert rgb.min() >= 0
    assert rgb.max() <= 255


def test_apply_palette_unknown_name_raises():
    with pytest.raises(ValueError):
        apply_palette(np.zeros((2, 2)), "not-a-real-palette")
