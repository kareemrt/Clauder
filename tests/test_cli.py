import os

from PIL import Image

from fractalforge.cli import main


def test_mandelbrot_cli(tmp_path):
    out = tmp_path / "mandelbrot.png"
    main(["mandelbrot", "-o", str(out), "--width", "20", "--height", "15", "--max-iter", "20"])
    assert out.exists()
    assert Image.open(out).size == (20, 15)


def test_julia_cli(tmp_path):
    out = tmp_path / "julia.png"
    main(["julia", "-o", str(out), "--width", "20", "--height", "15", "--max-iter", "20"])
    assert out.exists()


def test_burning_ship_cli(tmp_path):
    out = tmp_path / "ship.png"
    main(["burning-ship", "-o", str(out), "--width", "20", "--height", "15", "--max-iter", "20"])
    assert out.exists()


def test_sierpinski_cli(tmp_path):
    out = tmp_path / "sierpinski.png"
    main(["sierpinski", "-o", str(out), "--width", "20", "--height", "15", "--points", "200", "--seed", "1"])
    assert out.exists()


def test_fern_cli(tmp_path):
    out = tmp_path / "fern.png"
    main(["fern", "-o", str(out), "--width", "20", "--height", "15", "--points", "200", "--seed", "1"])
    assert out.exists()


def test_koch_cli(tmp_path):
    out = tmp_path / "koch.png"
    main(["koch", "-o", str(out), "--width", "20", "--height", "15", "--order", "2"])
    assert out.exists()


def test_zoom_cli(tmp_path):
    out = tmp_path / "zoom.gif"
    main(["zoom", "-o", str(out), "--width", "16", "--height", "12", "--frames", "2", "--max-iter", "20"])
    assert out.exists()


def test_palettes_cli(capsys):
    main(["palettes"])
    captured = capsys.readouterr()
    assert "fire" in captured.out


def test_invalid_palette_choice():
    import pytest

    with pytest.raises(SystemExit):
        main(["mandelbrot", "-o", "out.png", "--palette", "not-real"])
