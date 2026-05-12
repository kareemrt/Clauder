"""Entity types and constants for Terrarium."""

# Cell type constants
EMPTY = 0
PLANT = 1
HERBIVORE = 2
CARNIVORE = 3
WATER = 4
ROCK = 5


class Plant:
    __slots__ = ["energy", "age"]

    SPREAD_CHANCE = 0.12   # fast spread to sustain herbivore grazing
    DEATH_CHANCE = 0.002
    MAX_AGE = 300
    INITIAL_ENERGY = 8

    def __init__(self, energy: float = None):
        self.energy = energy if energy is not None else self.INITIAL_ENERGY
        self.age = 0


class Herbivore:
    __slots__ = ["energy", "age"]

    INITIAL_ENERGY = 30.0
    MAX_ENERGY = 80.0
    MAX_AGE = 200
    REPRODUCE_THRESHOLD = 78.0   # needs ~4 plant-eats from spawn to breed
    REPRODUCE_COST = 38.0        # baby starts at 19 energy (5+ eats to breed)
    MOVE_COST = 0.5
    EAT_GAIN = 12.0
    IDLE_COST = 0.18
    VISION = 4

    def __init__(self, energy: float = None):
        self.energy = energy if energy is not None else self.INITIAL_ENERGY
        self.age = 0


class Carnivore:
    __slots__ = ["energy", "age"]

    INITIAL_ENERGY = 45.0
    MAX_ENERGY = 100.0
    MAX_AGE = 220
    REPRODUCE_THRESHOLD = 95.0   # needs 4 kills from spawn to breed
    REPRODUCE_COST = 52.0
    MOVE_COST = 1.0
    EAT_GAIN = 15.0
    IDLE_COST = 0.65
    HUNT_RANGE = 5               # shorter range = harder to find sparse prey

    def __init__(self, energy: float = None):
        self.energy = energy if energy is not None else self.INITIAL_ENERGY
        self.age = 0
