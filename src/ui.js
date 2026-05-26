// Wires up the UI controls, initializes simulation & renderer, runs the app.

(function () {
  const canvas = document.getElementById('canvas');
  const sim    = new Simulation(canvas);
  const ren    = new Renderer(canvas, sim);

  // Resize canvas first, then start
  ren.resize();
  window.addEventListener('resize', () => ren.resize());

  // ── Helpers ────────────────────────────────────────────────────────────────

  function loadPreset(key) {
    let preset = key === 'random' ? generateRandomPreset() : PRESETS[key];
    if (!preset) preset = generateRandomPreset();

    sim.load(preset);
    ren.setPreset(preset);

    // Sync sliders to preset defaults
    setSlider('count',    preset.count);
    setSlider('range',    preset.range);
    setSlider('friction', preset.friction);

    buildLegend(preset.species);
    updateStatSpecies(preset.species.length);
  }

  function setSlider(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    el.value = value;
    el.dispatchEvent(new Event('input'));
  }

  function buildLegend(species) {
    const el = document.getElementById('legend');
    el.innerHTML = species.map(s =>
      `<div class="legend-item">
         <div class="legend-dot" style="background:${s.color};box-shadow:0 0 6px ${s.color}"></div>
         ${s.name.toUpperCase()}
       </div>`
    ).join('');
  }

  function updateStatSpecies(n) {
    document.getElementById('stat-species').textContent = n;
  }

  // ── Preset buttons ─────────────────────────────────────────────────────────

  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadPreset(btn.dataset.preset);
    });
  });

  // ── Sliders ────────────────────────────────────────────────────────────────

  function bindSlider(id, displayId, transform, onChange) {
    const el  = document.getElementById(id);
    const disp = document.getElementById(displayId);
    el.addEventListener('input', () => {
      const v = parseFloat(el.value);
      disp.textContent = transform(v);
      onChange(v);
    });
  }

  bindSlider('count',    'count-val',    v => v,                  v => { sim.params.count = v; sim.reset(); });
  bindSlider('speed',    'speed-val',    v => v.toFixed(1) + 'x', v => { sim.params.speed = v; });
  bindSlider('range',    'range-val',    v => v,                  v => { sim.params.range = v; });
  bindSlider('friction', 'friction-val', v => v.toFixed(2),       v => { sim.params.friction = v; });
  bindSlider('glow',     'glow-val',     v => v,                  v => { ren.params.glow = v; });
  bindSlider('trail',    'trail-val',    v => v.toFixed(2),       v => { ren.params.trail = v; });
  bindSlider('size',     'size-val',     v => v,                  v => { ren.params.size = v; });

  // ── Action buttons ─────────────────────────────────────────────────────────

  document.getElementById('btn-reset').addEventListener('click', () => {
    sim.reset();
    ren._clearFull && ren._clearFull();
  });

  const pauseBtn = document.getElementById('btn-pause');
  pauseBtn.addEventListener('click', () => {
    sim.paused = !sim.paused;
    pauseBtn.textContent = sim.paused ? '▶ Play' : '⏸ Pause';
  });

  document.getElementById('btn-screenshot').addEventListener('click', () => ren.screenshot());

  // ── Canvas click = energy burst ────────────────────────────────────────────

  canvas.addEventListener('click', e => {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left);
    const y = (e.clientY - rect.top);
    sim.burst(x, y);
  });

  // ── Stats loop ─────────────────────────────────────────────────────────────

  setInterval(() => {
    document.getElementById('fps').textContent         = ren.fps;
    document.getElementById('stat-count').textContent  = sim.particles.length;
  }, 500);

  // ── Boot ───────────────────────────────────────────────────────────────────

  loadPreset('cells');
  ren.start();

})();
