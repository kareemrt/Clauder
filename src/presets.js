// Particle species colors
const SPECIES_COLORS = [
  '#ff6b6b', // 0 Red
  '#ffa94d', // 1 Orange
  '#ffd43b', // 2 Yellow
  '#69db7c', // 3 Green
  '#74c0fc', // 4 Blue
  '#da77f2', // 5 Purple
];

const SPECIES_NAMES = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple'];

// Each preset is a 6x6 interaction matrix.
// matrix[i][j] = force that species j exerts on species i
// Positive = attraction, Negative = repulsion
const PRESETS = {
  cells: {
    name: 'Cells',
    description: 'Particles cluster into cell-like groups, each species forming tight communities while repelling others.',
    matrix: [
    //  R      O      Y      G      B      P
      [ 0.5,  -0.3,  -0.3,  -0.3,  -0.3,  -0.3], // R
      [-0.3,   0.5,  -0.3,  -0.3,  -0.3,  -0.3], // O
      [-0.3,  -0.3,   0.5,  -0.3,  -0.3,  -0.3], // Y
      [-0.3,  -0.3,  -0.3,   0.5,  -0.3,  -0.3], // G
      [-0.3,  -0.3,  -0.3,  -0.3,   0.5,  -0.3], // B
      [-0.3,  -0.3,  -0.3,  -0.3,  -0.3,   0.5], // P
    ],
  },

  galaxy: {
    name: 'Galaxy',
    description: 'Cascading attractions form swirling galactic arms and spinning nebulae.',
    matrix: [
    //  R      O      Y      G      B      P
      [ 0.3,   0.6,  -0.4,   0.1,   0.0,  -0.2], // R
      [-0.4,   0.3,   0.6,  -0.4,   0.1,   0.0], // O
      [ 0.0,  -0.4,   0.3,   0.6,  -0.4,   0.1], // Y
      [ 0.1,   0.0,  -0.4,   0.3,   0.6,  -0.4], // G
      [-0.4,   0.1,   0.0,  -0.4,   0.3,   0.6], // B
      [ 0.6,  -0.4,   0.1,   0.0,  -0.4,   0.3], // P
    ],
  },

  ecology: {
    name: 'Ecology',
    description: 'Predator-prey dynamics create a living ecosystem with chase and flee behaviors.',
    matrix: [
    //  R      O      Y      G      B      P
      [ 0.4,   0.7,  -0.5,   0.2,  -0.3,   0.1], // R
      [-0.6,   0.3,   0.6,  -0.3,   0.1,  -0.2], // O
      [ 0.2,  -0.5,   0.3,   0.7,  -0.4,   0.0], // Y
      [-0.2,   0.1,  -0.6,   0.3,   0.6,  -0.3], // G
      [ 0.3,  -0.2,   0.1,  -0.5,   0.3,   0.7], // B
      [-0.4,   0.3,  -0.2,   0.1,  -0.6,   0.3], // P
    ],
  },

  predators: {
    name: 'Predators',
    description: 'A food chain: Red eats Orange, Orange eats Yellow... creating a cycle of pursuit.',
    matrix: [
    //  R      O      Y      G      B      P
      [ 0.3,   0.8,  -0.6,   0.0,   0.0,  -0.6], // R hunts O, flees P
      [-0.6,   0.3,   0.8,  -0.6,   0.0,   0.0], // O hunts Y, flees R
      [ 0.0,  -0.6,   0.3,   0.8,  -0.6,   0.0], // Y hunts G, flees O
      [ 0.0,   0.0,  -0.6,   0.3,   0.8,  -0.6], // G hunts B, flees Y
      [-0.6,   0.0,   0.0,  -0.6,   0.3,   0.8], // B hunts P, flees G
      [ 0.8,  -0.6,   0.0,   0.0,  -0.6,   0.3], // P hunts R, flees B
    ],
  },

  harmony: {
    name: 'Harmony',
    description: 'All species gently attract each other, forming one flowing, unified dance.',
    matrix: [
    //  R      O      Y      G      B      P
      [ 0.5,   0.3,   0.2,   0.3,   0.2,   0.3], // R
      [ 0.3,   0.5,   0.3,   0.2,   0.3,   0.2], // O
      [ 0.2,   0.3,   0.5,   0.3,   0.2,   0.3], // Y
      [ 0.3,   0.2,   0.3,   0.5,   0.3,   0.2], // G
      [ 0.2,   0.3,   0.2,   0.3,   0.5,   0.3], // B
      [ 0.3,   0.2,   0.3,   0.2,   0.3,   0.5], // P
    ],
  },

  chaos: {
    name: 'Chaos',
    description: 'Unpredictable asymmetric rules create turbulent, explosive patterns.',
    matrix: [
    //  R      O      Y      G      B      P
      [ 0.7,  -0.8,   0.5,  -0.3,   0.6,  -0.9], // R
      [ 0.4,   0.6,  -0.7,   0.8,  -0.5,   0.3], // O
      [-0.6,   0.3,   0.8,  -0.4,   0.7,  -0.2], // Y
      [ 0.9,  -0.5,   0.2,   0.5,  -0.8,   0.4], // G
      [-0.3,   0.7,  -0.6,   0.3,   0.6,  -0.7], // B
      [ 0.5,  -0.2,   0.8,  -0.6,   0.3,   0.7], // P
    ],
  },
};
