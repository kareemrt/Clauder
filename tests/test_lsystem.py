from dataclasses import replace

from fracta.lsystem import PRESETS, expand, render_lsystem


def test_expand_koch_grows_by_rule():
    system = replace(PRESETS["koch"], iterations=1)
    assert expand(system) == "F+F-F-F+F"


def test_expand_length_grows_each_iteration():
    lengths = [len(expand(replace(PRESETS["koch"], iterations=n))) for n in range(1, 4)]
    assert lengths[0] < lengths[1] < lengths[2]


def test_render_all_presets_produce_nonempty_image():
    for name in PRESETS:
        img = render_lsystem(preset=name, width=100, height=100)
        assert img.size == (100, 100)
