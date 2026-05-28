"""Famous fractal locations — curated gallery of mathematical beauty."""

from dataclasses import dataclass


@dataclass
class Preset:
    name: str
    description: str
    fractal: str          # "mandelbrot" | "julia" | "burning_ship" | "newton" | "tricorn"
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    max_iter: int
    palette: str
    julia_c: complex | None = None  # only for julia presets


MANDELBROT_PRESETS: list[Preset] = [
    Preset(
        name="Full Mandelbrot",
        description="The classic overview — the entire Mandelbrot set in one view.",
        fractal="mandelbrot",
        xmin=-2.5, xmax=1.0, ymin=-1.25, ymax=1.25,
        max_iter=256, palette="fire",
    ),
    Preset(
        name="Seahorse Valley",
        description="Spiraling seahorse-shaped filaments along the main cardioid boundary.",
        fractal="mandelbrot",
        xmin=-0.7746806106269039, xmax=-0.7746806106269039 + 0.0015,
        ymin=0.1340379509481677, ymax=0.1340379509481677 + 0.0015,
        max_iter=1024, palette="ocean",
    ),
    Preset(
        name="Elephant Valley",
        description="Repeating elephant-trunk spirals near the period-3 bulb.",
        fractal="mandelbrot",
        xmin=0.2549870375144766, xmax=0.2549870375144766 + 0.0016,
        ymin=-0.0005, ymax=-0.0005 + 0.0016,
        max_iter=512, palette="galaxy",
    ),
    Preset(
        name="Starfish",
        description="A five-fold symmetric starfish emerging from cascading bifurcations.",
        fractal="mandelbrot",
        xmin=-0.3750001200919413, xmax=-0.3750001200919413 + 2e-5,
        ymin=0.6693685880058655, ymax=0.6693685880058655 + 2e-5,
        max_iter=2048, palette="psychedelic",
    ),
    Preset(
        name="Lightning Tendrils",
        description="Charged filaments radiating like lightning into the complex plane.",
        fractal="mandelbrot",
        xmin=-0.16070135, xmax=-0.16070135 + 5e-7,
        ymin=1.0376930, ymax=1.0376930 + 5e-7,
        max_iter=4096, palette="electric",
    ),
    Preset(
        name="Miniature Mandelbrot",
        description="A perfect mini-copy of the full set, infinitely nested within itself.",
        fractal="mandelbrot",
        xmin=-1.9415327994671, xmax=-1.9415327994671 + 2e-4,
        ymin=-0.0000081, ymax=-0.0000081 + 2e-4,
        max_iter=512, palette="fire",
    ),
]

JULIA_PRESETS: list[Preset] = [
    Preset(
        name="Douady Rabbit",
        description="Three interlocked spiraling rabbit ears — Douady's classic Julia set.",
        fractal="julia",
        xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5,
        max_iter=256, palette="psychedelic",
        julia_c=complex(-0.1226, 0.7449),
    ),
    Preset(
        name="San Marco Dragon",
        description="A basilica-like structure with two-fold symmetry.",
        fractal="julia",
        xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5,
        max_iter=256, palette="fire",
        julia_c=complex(-0.7269, 0.1889),
    ),
    Preset(
        name="Dendrite",
        description="Crystalline dendrite growing along the imaginary axis.",
        fractal="julia",
        xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5,
        max_iter=512, palette="ocean",
        julia_c=complex(0.0, 1.0),
    ),
    Preset(
        name="Siegel Disk",
        description="Smooth quasi-periodic rotation disk surrounded by chaotic filaments.",
        fractal="julia",
        xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5,
        max_iter=256, palette="galaxy",
        julia_c=complex(-0.3905, -0.5875),
    ),
    Preset(
        name="Snowflake",
        description="Six-fold symmetric snowflake Julia set — rare among quadratic maps.",
        fractal="julia",
        xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5,
        max_iter=256, palette="electric",
        julia_c=complex(-1.755, 0.0),
    ),
]

EXOTIC_PRESETS: list[Preset] = [
    Preset(
        name="Burning Ship",
        description="The ghostly burning ship — absolute-value fold creates haunting geometry.",
        fractal="burning_ship",
        xmin=-2.0, xmax=1.0, ymin=-2.0, ymax=0.8,
        max_iter=256, palette="fire",
    ),
    Preset(
        name="Newton's Basins",
        description="Three-basin attraction zones of Newton's method on z³ = 1.",
        fractal="newton",
        xmin=-2.0, xmax=2.0, ymin=-2.0, ymax=2.0,
        max_iter=64, palette="newton",
    ),
    Preset(
        name="Tricorn",
        description="The Mandelbar set — conjugate iteration creates thorny anti-fractals.",
        fractal="tricorn",
        xmin=-2.5, xmax=1.0, ymin=-1.25, ymax=1.25,
        max_iter=256, palette="galaxy",
    ),
]

ALL_PRESETS = MANDELBROT_PRESETS + JULIA_PRESETS + EXOTIC_PRESETS
