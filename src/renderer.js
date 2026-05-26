// Canvas 2D renderer with persistent trails, glow effects, and per-species colors.

class Renderer {
  constructor(canvas, sim) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.sim = sim;
    this.params = {
      glow: 12,
      trail: 0.18,
      size: 2.5,
    };
    this._fpsFrames = 0;
    this._fpsLast = performance.now();
    this._fps = 0;
    this._speciesColors = [];
    this._running = false;
    this._rafId = null;
  }

  start() {
    this._running = true;
    this._loop();
  }

  stop() {
    this._running = false;
    if (this._rafId) cancelAnimationFrame(this._rafId);
  }

  setPreset(preset) {
    this._speciesColors = preset.species.map(s => s.color);
    this._clearFull();
  }

  _clearFull() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.fillStyle = '#07080f';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  resize() {
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width  = Math.floor(window.innerWidth  * dpr);
    this.canvas.height = Math.floor(window.innerHeight * dpr);
    this.canvas.style.width  = window.innerWidth  + 'px';
    this.canvas.style.height = window.innerHeight + 'px';
    this.ctx.scale(dpr, dpr);
    this._clearFull();
  }

  _loop() {
    if (!this._running) return;
    this._rafId = requestAnimationFrame(() => this._loop());
    this.sim.tick();
    this._draw();
    this._updateFps();
  }

  _draw() {
    const ctx = this.ctx;
    const W = this.canvas.width / (window.devicePixelRatio || 1);
    const H = this.canvas.height / (window.devicePixelRatio || 1);
    const { glow, trail, size } = this.params;
    const colors = this._speciesColors;

    // Fade previous frame — this creates the trail effect
    ctx.globalAlpha = trail;
    ctx.fillStyle = '#07080f';
    ctx.fillRect(0, 0, W, H);
    ctx.globalAlpha = 1.0;

    // Glow pass
    if (glow > 0) {
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      for (const p of this.sim.particles) {
        const color = colors[p.species] || '#ffffff';
        ctx.shadowColor = color;
        ctx.shadowBlur  = glow;
        ctx.fillStyle   = color;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        ctx.arc(p.x, p.y, size * 0.6, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }

    // Core particles
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.shadowBlur = 0;
    ctx.globalAlpha = 0.95;
    for (const p of this.sim.particles) {
      ctx.fillStyle = colors[p.species] || '#ffffff';
      ctx.beginPath();
      ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  _updateFps() {
    this._fpsFrames++;
    const now = performance.now();
    if (now - this._fpsLast > 500) {
      this._fps = Math.round(this._fpsFrames / ((now - this._fpsLast) / 1000));
      this._fpsFrames = 0;
      this._fpsLast = now;
    }
  }

  get fps() { return this._fps; }

  screenshot() {
    const link = document.createElement('a');
    link.download = `quantumdrift-${Date.now()}.png`;
    link.href = this.canvas.toDataURL('image/png');
    link.click();
  }
}
