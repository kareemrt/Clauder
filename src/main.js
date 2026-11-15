// ── Particle Life — main.js ──────────────────────────────────────────────────

const canvas = document.getElementById('canvas');
let sim;

function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}

// ── Init ─────────────────────────────────────────────────────────────────────

function init() {
  resizeCanvas();
  window.addEventListener('resize', () => {
    resizeCanvas();
    if (sim) {
      sim.canvas = canvas;
      sim.scatter();
    }
  });

  const particles = parseInt(document.getElementById('particles-slider').value, 10);
  sim = new ParticleLife(canvas, particles);

  buildLegend();
  buildMatrixViz();
  bindControls();
  hideTooltipSoon();
  requestAnimationFrame(loop);
}

// ── Main loop ─────────────────────────────────────────────────────────────────

let lastTime = performance.now();
let speedMultiplier = 1.0;
let trailAlpha = 0.25;

function loop(now) {
  const rawDt = (now - lastTime) / 1000;
  lastTime = now;
  const dt = rawDt * speedMultiplier;

  sim.update(dt);
  sim.render(trailAlpha);
  sim.trackFPS(now);

  document.getElementById('fps-counter').textContent   = sim.fps + ' fps';
  document.getElementById('particle-count').textContent = sim.n + ' particles';

  requestAnimationFrame(loop);
}

// ── Controls ──────────────────────────────────────────────────────────────────

function bindControls() {
  // Preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const key = btn.dataset.preset;
      sim.setPreset(key);
      updatePresetDesc(key);
      buildMatrixViz();
    });
  });

  // Particle count
  const pSlider = document.getElementById('particles-slider');
  const pVal    = document.getElementById('particles-val');
  pSlider.addEventListener('input', () => {
    pVal.textContent = pSlider.value;
  });
  pSlider.addEventListener('change', () => {
    sim.resize(parseInt(pSlider.value, 10));
  });

  // Speed
  const sSlider = document.getElementById('speed-slider');
  const sVal    = document.getElementById('speed-val');
  sSlider.addEventListener('input', () => {
    speedMultiplier = parseInt(sSlider.value, 10) / 10;
    sVal.textContent = speedMultiplier.toFixed(1) + '×';
  });

  // Radius
  const rSlider = document.getElementById('radius-slider');
  const rVal    = document.getElementById('radius-val');
  rSlider.addEventListener('input', () => {
    const v = parseInt(rSlider.value, 10);
    rVal.textContent = v;
    sim.setMaxDist(v);
  });

  // Friction
  const fSlider = document.getElementById('friction-slider');
  const fVal    = document.getElementById('friction-val');
  fSlider.addEventListener('input', () => {
    const v = parseInt(fSlider.value, 10) / 100;
    fVal.textContent = v.toFixed(2);
    sim.friction = v;
  });

  // Buttons
  document.getElementById('btn-randomize').addEventListener('click', () => {
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
    sim.randomizeRules();
    updatePresetDesc(null);
    buildMatrixViz();
  });

  document.getElementById('btn-scatter').addEventListener('click', () => {
    sim.scatter();
  });

  const pauseBtn = document.getElementById('btn-pause');
  pauseBtn.addEventListener('click', () => {
    sim.paused = !sim.paused;
    pauseBtn.textContent = sim.paused ? '▶ Resume' : '⏸ Pause';
    pauseBtn.classList.toggle('paused', sim.paused);
    if (!sim.paused) {
      lastTime = performance.now();
    }
  });

  // Click on canvas spawns particles
  canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    // Spawn 20 random particles at click point
    for (let i = 0; i < 20; i++) {
      sim.spawnAt(x + (Math.random() - 0.5) * 40, y + (Math.random() - 0.5) * 40);
    }
  });

  // Initial preset description
  updatePresetDesc('cells');
}

function updatePresetDesc(key) {
  const el = document.getElementById('preset-desc');
  if (key && PRESETS[key]) {
    el.textContent = '"' + PRESETS[key].description + '"';
  } else {
    el.textContent = '"Rules randomized — unique emergent behavior every time."';
  }
}

// ── Legend ────────────────────────────────────────────────────────────────────

function buildLegend() {
  const container = document.getElementById('legend-items');
  container.innerHTML = '';
  SPECIES_COLORS.forEach((color, i) => {
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `
      <div class="legend-dot" style="background:${color}"></div>
      <span>${SPECIES_NAMES[i]}</span>
    `;
    container.appendChild(item);
  });
}

// ── Matrix Visualization ──────────────────────────────────────────────────────

function buildMatrixViz() {
  const mc = document.getElementById('matrix-canvas');
  const ctx = mc.getContext('2d');
  const n = SPECIES_COLORS.length;
  const cellW = mc.width  / (n + 1);
  const cellH = mc.height / (n + 1);

  ctx.clearRect(0, 0, mc.width, mc.height);

  if (!sim || !sim.matrix) return;

  // Draw species header dots
  for (let i = 0; i < n; i++) {
    // Column header
    ctx.fillStyle = SPECIES_COLORS[i];
    ctx.beginPath();
    ctx.arc((i + 1.5) * cellW, cellH * 0.5, 4, 0, 6.2832);
    ctx.fill();
    // Row header
    ctx.beginPath();
    ctx.arc(cellW * 0.5, (i + 1.5) * cellH, 4, 0, 6.2832);
    ctx.fill();
  }

  // Draw matrix cells
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const val = sim.matrix[i][j];
      const x = (j + 1) * cellW;
      const y = (i + 1) * cellH;

      // Background rect
      const alpha = Math.abs(val) * 0.9;
      if (val > 0) {
        ctx.fillStyle = `rgba(100, 220, 100, ${alpha})`;
      } else {
        ctx.fillStyle = `rgba(220, 80, 80, ${alpha})`;
      }
      ctx.fillRect(x + 1, y + 1, cellW - 2, cellH - 2);
    }
  }

  // Grid lines
  ctx.strokeStyle = 'rgba(255,255,255,0.08)';
  ctx.lineWidth = 0.5;
  for (let i = 1; i <= n + 1; i++) {
    ctx.beginPath();
    ctx.moveTo(i * cellW, cellH);
    ctx.lineTo(i * cellW, mc.height);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cellW, i * cellH);
    ctx.lineTo(mc.width, i * cellH);
    ctx.stroke();
  }

  // Label
  ctx.fillStyle = 'rgba(108, 112, 134, 0.8)';
  ctx.font = '8px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('↓ attracted by', mc.width / 2, mc.height - 2);
}

// ── Tooltip ───────────────────────────────────────────────────────────────────

function hideTooltipSoon() {
  setTimeout(() => {
    const t = document.getElementById('tooltip');
    if (t) t.classList.add('hidden');
  }, 4000);
}

// ── Keyboard shortcuts ────────────────────────────────────────────────────────

document.addEventListener('keydown', (e) => {
  switch (e.key) {
    case ' ':
      e.preventDefault();
      document.getElementById('btn-pause').click();
      break;
    case 'r':
    case 'R':
      document.getElementById('btn-randomize').click();
      break;
    case 's':
    case 'S':
      document.getElementById('btn-scatter').click();
      break;
    case '1': case '2': case '3': case '4': case '5': case '6': {
      const keys = Object.keys(PRESETS);
      const idx  = parseInt(e.key) - 1;
      if (keys[idx]) document.querySelector(`[data-preset="${keys[idx]}"]`)?.click();
      break;
    }
  }
});

// ── Start ─────────────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', init);
