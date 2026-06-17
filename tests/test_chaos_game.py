import numpy as np

from fracta.chaos_game import PRESETS, render_chaos_game, run_chaos_game


def test_run_chaos_game_point_count():
    points = run_chaos_game(PRESETS["sierpinski_triangle"], n_points=1000, warmup=10)
    assert points.shape == (1000, 2)


def test_run_chaos_game_is_deterministic_with_seed():
    p1 = run_chaos_game(PRESETS["barnsley_fern"], n_points=500, seed=42)
    p2 = run_chaos_game(PRESETS["barnsley_fern"], n_points=500, seed=42)
    assert np.array_equal(p1, p2)


def test_render_chaos_game_shape():
    img = render_chaos_game(preset="sierpinski_triangle", width=64, height=64, n_points=2000)
    assert img.shape == (64, 64, 3)
    assert img.dtype == np.uint8
