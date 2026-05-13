from .mandelbrot import mandelbrot
from .julia import julia
from .burning_ship import burning_ship

FRACTALS = {
    "mandelbrot": mandelbrot,
    "julia": julia,
    "burning_ship": burning_ship,
}
