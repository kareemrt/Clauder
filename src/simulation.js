// Particle Life simulation engine.
// Each particle belongs to a species. Forces between species are defined
// by the preset's interaction matrix — positive = attraction, negative = repulsion.
// A short-range repulsion term prevents total collapse regardless of the matrix.

class Simulation {
  constructor(canvas) {
    this.canvas = canvas;
    this.particles = [];
    this.preset = null;
    this.params = {
      count: 600,
      range: 80,
      friction: 0.85,
      speed: 1.0,
    };
    this.paused = false;
    this.tickCount = 0;
  }

  load(preset) {
    this.preset = preset;
    this.params.count = preset.count;
    this.params.range = preset.range;
    this.params.friction = preset.friction;
    this.reset();
  }

  reset() {
    const { count } = this.params;
    const n = this.preset.species.length;
    const W = this.canvas.width;
    const H = this.canvas.height;

    this.particles = Array.from({ length: count }, (_, i) => ({
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 1.5,
      vy: (Math.random() - 0.5) * 1.5,
      species: i % n,
    }));

    this.tickCount = 0;
  }

  // Add an energy burst at (cx, cy) — pushes nearby particles outward
  burst(cx, cy, radius = 150, strength = 4) {
    for (const p of this.particles) {
      const dx = p.x - cx;
      const dy = p.y - cy;
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < radius && d > 0.1) {
        const f = (1 - d / radius) * strength;
        p.vx += (dx / d) * f;
        p.vy += (dy / d) * f;
      }
    }
  }

  tick() {
    if (this.paused) return;

    const ps = this.particles;
    const n = ps.length;
    const matrix = this.preset.matrix;
    const R = this.params.range;
    const R2 = R * R;
    const friction = this.params.friction;
    const speed = this.params.speed;
    const W = this.canvas.width;
    const H = this.canvas.height;
    const RMIN = 12;  // short-range repulsion radius
    const RMIN2 = RMIN * RMIN;

    // Compute forces (O(N²) — fast enough for N≤1500 at 60fps)
    for (let i = 0; i < n; i++) {
      let fx = 0;
      let fy = 0;
      const pi = ps[i];

      for (let j = 0; j < n; j++) {
        if (i === j) continue;
        const pj = ps[j];

        let dx = pj.x - pi.x;
        let dy = pj.y - pi.y;

        // Toroidal wrap — measure shortest distance
        if (dx > W * 0.5) dx -= W;
        else if (dx < -W * 0.5) dx += W;
        if (dy > H * 0.5) dy -= H;
        else if (dy < -H * 0.5) dy += H;

        const d2 = dx * dx + dy * dy;
        if (d2 > R2 || d2 < 0.01) continue;

        const d = Math.sqrt(d2);

        // Short-range universal repulsion (prevents clumping)
        let force;
        if (d2 < RMIN2) {
          force = -1.0 * (RMIN / d - 1.0);
        } else {
          // Smooth ramp: rises to peak at R/3, falls back to 0 at R
          const norm = d / R;
          const peak = R * 0.33;
          if (d < peak) {
            force = matrix[pi.species][pj.species] * (d / peak);
          } else {
            force = matrix[pi.species][pj.species] * (1.0 - norm) / (1.0 - peak / R);
          }
        }

        const inv = force / d;
        fx += dx * inv;
        fy += dy * inv;
      }

      pi.vx = (pi.vx + fx * 0.04 * speed) * friction;
      pi.vy = (pi.vy + fy * 0.04 * speed) * friction;
    }

    // Integrate positions with toroidal wrap
    for (const p of ps) {
      p.x += p.vx * speed;
      p.y += p.vy * speed;
      if (p.x < 0) p.x += W;
      else if (p.x >= W) p.x -= W;
      if (p.y < 0) p.y += H;
      else if (p.y >= H) p.y -= H;
    }

    this.tickCount++;
  }
}
