// Spatial hash grid for O(n·k) nearest-neighbor queries
class SpatialGrid {
  constructor(width, height, cellSize) {
    this.width = width;
    this.height = height;
    this.cellSize = cellSize;
    this.cols = Math.ceil(width / cellSize) + 1;
    this.rows = Math.ceil(height / cellSize) + 1;
    this.cells = new Array(this.cols * this.rows);
    for (let i = 0; i < this.cells.length; i++) this.cells[i] = [];
  }

  clear() {
    for (let i = 0; i < this.cells.length; i++) this.cells[i].length = 0;
  }

  _idx(col, row) {
    const c = ((col % this.cols) + this.cols) % this.cols;
    const r = ((row % this.rows) + this.rows) % this.rows;
    return r * this.cols + c;
  }

  insert(x, y, particleIdx) {
    const col = Math.floor(x / this.cellSize);
    const row = Math.floor(y / this.cellSize);
    this.cells[this._idx(col, row)].push(particleIdx);
  }

  getNearby(x, y, out) {
    out.length = 0;
    const col = Math.floor(x / this.cellSize);
    const row = Math.floor(y / this.cellSize);
    for (let dr = -1; dr <= 1; dr++) {
      for (let dc = -1; dc <= 1; dc++) {
        const cell = this.cells[this._idx(col + dc, row + dr)];
        for (let i = 0; i < cell.length; i++) out.push(cell[i]);
      }
    }
  }
}

class ParticleLife {
  constructor(canvas, numParticles = 1200) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: false });
    this.numSpecies = SPECIES_COLORS.length; // 6
    this.maxDist = 80;
    this.minDist = 12;
    this.friction = 0.05;
    this.forceMult = 1.0;
    this.paused = false;
    this.matrix = null;

    this._nearbyBuf = [];
    this._resize(numParticles);
    this._initGrid();

    this._lastTime = performance.now();
    this._frameTimes = [];
    this.fps = 0;

    this._applyPreset('cells');
  }

  _resize(n) {
    this.n = n;
    this.x  = new Float32Array(n);
    this.y  = new Float32Array(n);
    this.vx = new Float32Array(n);
    this.vy = new Float32Array(n);
    this.sp = new Uint8Array(n);   // species index
  }

  _initGrid() {
    this.grid = new SpatialGrid(
      this.canvas.width,
      this.canvas.height,
      this.maxDist
    );
  }

  _applyPreset(key) {
    const preset = PRESETS[key];
    if (!preset) return;
    this.currentPreset = key;
    this.matrix = preset.matrix.map(row => [...row]);
    this.scatter();
  }

  setPreset(key) {
    this._applyPreset(key);
  }

  randomizeRules() {
    this.currentPreset = null;
    this.matrix = [];
    for (let i = 0; i < this.numSpecies; i++) {
      this.matrix[i] = [];
      for (let j = 0; j < this.numSpecies; j++) {
        this.matrix[i][j] = (Math.random() * 2 - 1) * 0.9;
      }
    }
  }

  scatter() {
    const W = this.canvas.width;
    const H = this.canvas.height;
    for (let i = 0; i < this.n; i++) {
      this.x[i]  = Math.random() * W;
      this.y[i]  = Math.random() * H;
      this.vx[i] = (Math.random() - 0.5) * 0.5;
      this.vy[i] = (Math.random() - 0.5) * 0.5;
      this.sp[i] = Math.floor(Math.random() * this.numSpecies);
    }
  }

  resize(numParticles) {
    this._resize(numParticles);
    this.scatter();
    this._initGrid();
  }

  spawnAt(x, y, species) {
    // Find a slot to reuse (simple: replace a random particle near edge)
    const idx = Math.floor(Math.random() * this.n);
    this.x[idx]  = x + (Math.random() - 0.5) * 10;
    this.y[idx]  = y + (Math.random() - 0.5) * 10;
    this.vx[idx] = 0;
    this.vy[idx] = 0;
    this.sp[idx] = species ?? Math.floor(Math.random() * this.numSpecies);
  }

  setMaxDist(v) {
    this.maxDist = v;
    this._initGrid();
  }

  update(dt) {
    if (this.paused) return;
    dt = Math.min(dt, 0.05); // cap to avoid spiral on tab switch

    const W = this.canvas.width;
    const H = this.canvas.height;
    const minD  = this.minDist;
    const maxD  = this.maxDist;
    const fMult = this.forceMult;
    const frict = this.friction;
    const n     = this.n;
    const mat   = this.matrix;

    // Rebuild spatial grid
    this.grid.width  = W;
    this.grid.height = H;
    this.grid.cellSize = maxD;
    this.grid.cols = Math.ceil(W / maxD) + 1;
    this.grid.rows = Math.ceil(H / maxD) + 1;
    if (this.grid.cells.length !== this.grid.cols * this.grid.rows) {
      this.grid.cells = new Array(this.grid.cols * this.grid.rows);
      for (let i = 0; i < this.grid.cells.length; i++) this.grid.cells[i] = [];
    }

    this.grid.clear();
    for (let i = 0; i < n; i++) this.grid.insert(this.x[i], this.y[i], i);

    const nearby = this._nearbyBuf;
    const halfW = W * 0.5;
    const halfH = H * 0.5;

    for (let i = 0; i < n; i++) {
      let ax = 0, ay = 0;
      const xi = this.x[i], yi = this.y[i];
      const si = this.sp[i];
      const matRow = mat[si];

      this.grid.getNearby(xi, yi, nearby);

      for (let ki = 0; ki < nearby.length; ki++) {
        const j = nearby[ki];
        if (j === i) continue;

        let dx = this.x[j] - xi;
        let dy = this.y[j] - yi;

        // Toroidal wrapping
        if (dx >  halfW) dx -= W;
        else if (dx < -halfW) dx += W;
        if (dy >  halfH) dy -= H;
        else if (dy < -halfH) dy += H;

        const dist2 = dx * dx + dy * dy;
        if (dist2 >= maxD * maxD || dist2 < 0.01) continue;

        const dist = Math.sqrt(dist2);
        let f = 0;

        if (dist < minD) {
          // Hard repulsion — same for all species pairs
          f = fMult * -1.5 * (minD / dist - 1);
        } else {
          // Rule-based force: triangular kernel peaking at midpoint
          const rule = matRow[this.sp[j]];
          const t = (dist - minD) / (maxD - minD); // 0..1
          const kernel = 1 - Math.abs(2 * t - 1);  // triangle
          f = fMult * rule * kernel;
        }

        const invD = 1 / dist;
        ax += f * dx * invD;
        ay += f * dy * invD;
      }

      this.vx[i] += ax * dt;
      this.vy[i] += ay * dt;

      // Friction
      const decay = 1 - frict;
      this.vx[i] *= decay;
      this.vy[i] *= decay;

      // Update position with toroidal wrapping
      this.x[i] = (this.x[i] + this.vx[i] * dt * 60 + W) % W;
      this.y[i] = (this.y[i] + this.vy[i] * dt * 60 + H) % H;
    }
  }

  render(trailAlpha) {
    const W = this.canvas.width;
    const H = this.canvas.height;
    const ctx = this.ctx;

    // Trail / fade effect
    ctx.fillStyle = `rgba(10, 10, 15, ${trailAlpha})`;
    ctx.fillRect(0, 0, W, H);

    // Draw particles
    const r = 2.5;
    for (let i = 0; i < this.n; i++) {
      ctx.fillStyle = SPECIES_COLORS[this.sp[i]];
      ctx.beginPath();
      ctx.arc(this.x[i], this.y[i], r, 0, 6.2832);
      ctx.fill();
    }
  }

  trackFPS(now) {
    this._frameTimes.push(now);
    while (this._frameTimes.length > 0 && now - this._frameTimes[0] > 1000) {
      this._frameTimes.shift();
    }
    this.fps = this._frameTimes.length;
  }
}
