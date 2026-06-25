"""Hand-rolled colormaps mapping a normalized value t in [0, 1] to RGB."""

import math


def _lerp(a, b, t):
    return a + (b - a) * t


def _gradient(stops):
    """Build a colormap function from a list of (position, (r, g, b)) stops."""

    def cmap(t):
        t = max(0.0, min(1.0, t))
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            if p0 <= t <= p1:
                local_t = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
                return tuple(
                    round(_lerp(c0[i], c1[i], local_t)) for i in range(3)
                )
        return stops[-1][1]

    return cmap


fire = _gradient([
    (0.00, (5, 0, 20)),
    (0.20, (60, 0, 80)),
    (0.45, (180, 20, 30)),
    (0.70, (240, 110, 10)),
    (0.88, (255, 210, 60)),
    (1.00, (255, 255, 230)),
])

ocean = _gradient([
    (0.00, (0, 5, 20)),
    (0.30, (0, 40, 90)),
    (0.55, (0, 110, 160)),
    (0.78, (40, 200, 210)),
    (1.00, (220, 250, 245)),
])

inferno = _gradient([
    (0.00, (0, 0, 4)),
    (0.25, (87, 16, 110)),
    (0.50, (188, 55, 84)),
    (0.75, (249, 142, 9)),
    (1.00, (252, 255, 164)),
])

grayscale = _gradient([
    (0.0, (0, 0, 0)),
    (1.0, (255, 255, 255)),
])


def psychedelic(t):
    r = round(127 + 127 * math.sin(2 * math.pi * (t + 0.00)))
    g = round(127 + 127 * math.sin(2 * math.pi * (t + 0.33)))
    b = round(127 + 127 * math.sin(2 * math.pi * (t + 0.67)))
    return (r, g, b)


CMAPS = {
    "fire": fire,
    "ocean": ocean,
    "inferno": inferno,
    "grayscale": grayscale,
    "psychedelic": psychedelic,
}


def get(name):
    try:
        return CMAPS[name]
    except KeyError:
        raise ValueError(f"unknown colormap '{name}', choose from {sorted(CMAPS)}")
