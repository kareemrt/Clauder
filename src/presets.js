// Presets define species colors and their attraction/repulsion matrices.
// matrix[i][j] = force that species i feels toward species j
// Positive = attraction, Negative = repulsion

const PRESETS = {

  cells: {
    name: "Cells",
    description: "Organic cell-like clustering with predator/prey dynamics",
    species: [
      { name: "Cytoplasm", color: "#4af0b0" },
      { name: "Nucleus",   color: "#4a7cff" },
      { name: "Membrane",  color: "#ff4a7c" },
      { name: "Mitochond", color: "#ffd04a" },
    ],
    // [from][to] — hand-crafted for organic cell behavior
    matrix: [
      [ 0.10,  0.50, -0.30,  0.20],
      [ 0.60,  0.05, -0.10,  0.40],
      [-0.20, -0.10,  0.30,  0.10],
      [ 0.30,  0.40, -0.20,  0.15],
    ],
    count: 600,
    range: 80,
    friction: 0.85,
  },

  predator: {
    name: "Predator",
    description: "Three-way predator-prey cycle — watch populations surge and crash",
    species: [
      { name: "Prey",     color: "#4af07a" },
      { name: "Predator", color: "#ff5a4a" },
      { name: "Apex",     color: "#c04aff" },
    ],
    matrix: [
      [ 0.15, -0.70,  0.10],
      [ 0.80,  0.05, -0.60],
      [ 0.10,  0.70,  0.05],
    ],
    count: 500,
    range: 100,
    friction: 0.88,
  },

  coral: {
    name: "Coral",
    description: "Branching coral-like growth patterns with symbiotic algae",
    species: [
      { name: "Coral",    color: "#ff7a4a" },
      { name: "Algae",    color: "#4aff9a" },
      { name: "Polyp",    color: "#ffcc4a" },
      { name: "Plankton", color: "#4ac8ff" },
      { name: "Mucus",    color: "#ff4abf" },
    ],
    matrix: [
      [ 0.20,  0.60,  0.40, -0.10,  0.10],
      [ 0.50,  0.10,  0.30,  0.20, -0.20],
      [ 0.40,  0.30,  0.15,  0.10,  0.30],
      [-0.10,  0.20,  0.10,  0.05,  0.40],
      [ 0.10, -0.10,  0.30,  0.50,  0.05],
    ],
    count: 700,
    range: 70,
    friction: 0.82,
  },

  galaxy: {
    name: "Galaxy",
    description: "Spiral arm formation — particles orbit like stellar systems",
    species: [
      { name: "Stars",    color: "#fffae0" },
      { name: "Dark",     color: "#6060ff" },
      { name: "Gas",      color: "#ff9060" },
      { name: "Plasma",   color: "#60ffff" },
    ],
    matrix: [
      [ 0.05,  0.30,  0.50,  0.10],
      [ 0.30,  0.02, -0.10,  0.60],
      [ 0.40, -0.20,  0.08,  0.30],
      [ 0.20,  0.50,  0.40,  0.04],
    ],
    count: 800,
    range: 120,
    friction: 0.92,
  },

  chaos: {
    name: "Chaos",
    description: "Maximum entropy — beautiful turbulent emergent patterns",
    species: [
      { name: "Alpha",   color: "#ff3366" },
      { name: "Beta",    color: "#33ffcc" },
      { name: "Gamma",   color: "#ffcc33" },
      { name: "Delta",   color: "#cc33ff" },
      { name: "Epsilon", color: "#33aaff" },
      { name: "Zeta",    color: "#ff8833" },
    ],
    matrix: [
      [ 0.10, -0.60,  0.70, -0.40,  0.30, -0.50],
      [ 0.80,  0.05, -0.50,  0.60, -0.30,  0.40],
      [-0.40,  0.70,  0.08, -0.60,  0.50, -0.20],
      [ 0.60, -0.30,  0.80,  0.06, -0.50,  0.40],
      [-0.20,  0.50, -0.30,  0.70,  0.07, -0.60],
      [ 0.50, -0.40,  0.30, -0.20,  0.80,  0.04],
    ],
    count: 900,
    range: 90,
    friction: 0.87,
  },

  random: null, // generated at runtime
};

function generateRandomPreset(numSpecies) {
  numSpecies = numSpecies || (3 + Math.floor(Math.random() * 4));
  const hues = Array.from({ length: numSpecies }, (_, i) =>
    Math.floor((i / numSpecies) * 360 + Math.random() * 40)
  );
  const species = hues.map((h, i) => ({
    name: `Species ${String.fromCharCode(65 + i)}`,
    color: `hsl(${h}, 80%, 60%)`,
  }));
  const matrix = Array.from({ length: numSpecies }, () =>
    Array.from({ length: numSpecies }, () => (Math.random() * 2 - 1) * 0.8)
  );
  return {
    name: "Random",
    description: "Randomly generated universe — every run is unique",
    species,
    matrix,
    count: 500 + Math.floor(Math.random() * 300),
    range: 60 + Math.floor(Math.random() * 80),
    friction: 0.80 + Math.random() * 0.15,
  };
}
