"""
Generate a beautiful, self-contained interactive HTML fractal explorer.
No external dependencies — pure Canvas + vanilla JS.
"""

import json
import math
import datetime
from .fractals import LANDMARKS
from .palettes import PALETTES


def _palette_to_js(name: str, stops: list) -> str:
    """Serialize a Python palette to a JS array literal."""
    arr = json.dumps([[r, g, b] for r, g, b in stops])
    return f'palettes["{name}"] = {arr};'


def generate_html(output_path: str = "mandelbrot_voyage.html") -> str:
    """
    Generate and write the interactive HTML file.
    Returns the path written.
    """
    # Serialize Python data into JS
    palettes_js = "\n    ".join(_palette_to_js(k, v) for k, v in PALETTES.items())
    landmarks_js = json.dumps({
        name: {k: v for k, v in loc.items()}
        for name, loc in LANDMARKS.items()
    }, indent=4)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mandelbrot Voyage — Interactive Fractal Explorer</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg:        #0a0a12;
    --surface:   #0f1118;
    --border:    #1e2330;
    --accent:    #4fc3f7;
    --accent2:   #81d4fa;
    --text:      #cdd6f4;
    --muted:     #6c7086;
    --green:     #a6e3a1;
    --red:       #f38ba8;
    --yellow:    #f9e2af;
    --radius:    8px;
    --font:      'Courier New', Courier, monospace;
  }}

  html, body {{
    height: 100%;
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 13px;
    overflow: hidden;
  }}

  /* ── Header ─────────────────────────────────────────────── */
  #header {{
    height: 46px;
    display: flex;
    align-items: center;
    padding: 0 16px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    gap: 12px;
    user-select: none;
  }}
  #logo {{
    font-size: 18px;
    font-weight: bold;
    color: var(--accent);
    letter-spacing: 1px;
  }}
  #logo span {{ color: var(--muted); font-weight: normal; font-size: 12px; }}
  #coords {{
    margin-left: auto;
    color: var(--muted);
    font-size: 11px;
    min-width: 340px;
    text-align: right;
  }}

  /* ── Layout ─────────────────────────────────────────────── */
  #main {{
    display: flex;
    height: calc(100vh - 46px);
  }}

  /* ── Canvas ─────────────────────────────────────────────── */
  #canvas-wrap {{
    position: relative;
    flex: 1;
    overflow: hidden;
    background: #000;
  }}
  canvas {{
    display: block;
    cursor: crosshair;
    image-rendering: pixelated;
  }}
  #progress-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    background: var(--accent);
    width: 0%;
    transition: width 0.1s;
  }}
  #rendering-badge {{
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 4px 10px;
    background: rgba(0,0,0,0.7);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 11px;
    color: var(--accent);
    display: none;
  }}

  /* ── Sidebar ─────────────────────────────────────────────── */
  #sidebar {{
    width: 260px;
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border-left: 1px solid var(--border);
    overflow-y: auto;
    flex-shrink: 0;
  }}

  .panel {{
    padding: 14px 14px 10px;
    border-bottom: 1px solid var(--border);
  }}
  .panel-title {{
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
  }}

  /* Buttons */
  button {{
    cursor: pointer;
    font-family: var(--font);
    font-size: 12px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 5px 10px;
    transition: border-color 0.15s, background 0.15s, color 0.15s;
    background: transparent;
    color: var(--text);
  }}
  button:hover {{ background: var(--border); }}
  button.active {{ background: var(--accent); color: #0a0a12; border-color: var(--accent); font-weight: bold; }}
  button.small {{ padding: 3px 8px; font-size: 11px; }}

  .btn-row {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 6px; }}

  /* Select */
  select {{
    font-family: var(--font);
    font-size: 12px;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 5px 8px;
    width: 100%;
    cursor: pointer;
  }}
  select:focus {{ outline: none; border-color: var(--accent); }}

  /* Slider */
  label.slider-label {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    color: var(--muted);
    font-size: 11px;
  }}
  input[type=range] {{
    width: 100%;
    accent-color: var(--accent);
    cursor: pointer;
    margin-bottom: 10px;
  }}

  /* Landmarks */
  #landmark-list {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  #landmark-list button {{
    text-align: left;
    padding: 6px 10px;
    width: 100%;
    font-size: 11px;
  }}
  #landmark-list button:hover {{ border-color: var(--accent); }}

  /* Stats */
  .stat-row {{ display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 11px; }}
  .stat-key {{ color: var(--muted); }}
  .stat-val {{ color: var(--green); font-variant-numeric: tabular-nums; }}

  /* Julia controls */
  #julia-params {{
    display: none;
    flex-direction: column;
    gap: 4px;
  }}
  #julia-params.visible {{ display: flex; }}

  /* Color strip preview */
  #palette-preview {{
    height: 14px;
    border-radius: 4px;
    margin-top: 8px;
    border: 1px solid var(--border);
    background: linear-gradient(to right,
      #000 0%, #000380 12%, #2068c8 30%, #edfeff 52%, #ffa800 70%, #001400 90%
    );
  }}

  /* Shortcut hint */
  #hints {{
    padding: 10px 14px;
    font-size: 10px;
    color: var(--muted);
    line-height: 1.8;
  }}
  kbd {{
    border: 1px solid var(--muted);
    border-radius: 3px;
    padding: 0 4px;
    font-size: 10px;
    color: var(--text);
  }}

  /* Help overlay */
  #help-overlay {{
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.82);
    z-index: 100;
    justify-content: center;
    align-items: center;
  }}
  #help-overlay.visible {{ display: flex; }}
  #help-box {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 36px;
    max-width: 480px;
    line-height: 2;
  }}
  #help-box h2 {{ color: var(--accent); margin-bottom: 16px; font-size: 16px; }}
  #help-box td:first-child {{ padding-right: 20px; }}
</style>
</head>
<body>

<div id="header">
  <div id="logo">🌀 Mandelbrot Voyage <span>— Interactive Fractal Explorer</span></div>
  <div id="coords">Hover over the canvas to see coordinates</div>
</div>

<div id="main">
  <div id="canvas-wrap">
    <canvas id="canvas"></canvas>
    <div id="progress-bar"></div>
    <div id="rendering-badge">⟳ Rendering…</div>
    <div id="help-overlay">
      <div id="help-box">
        <h2>⌨ Keyboard Shortcuts</h2>
        <table>
          <tr><td><kbd>Scroll</kbd> / <kbd>+</kbd> <kbd>−</kbd></td><td>Zoom in / out</td></tr>
          <tr><td><kbd>Drag</kbd></td><td>Pan view</td></tr>
          <tr><td><kbd>Click</kbd></td><td>Center on point</td></tr>
          <tr><td><kbd>R</kbd></td><td>Reset to full view</td></tr>
          <tr><td><kbd>H</kbd></td><td>Toggle this help</td></tr>
          <tr><td><kbd>↑</kbd> <kbd>↓</kbd></td><td>Increase / decrease iterations</td></tr>
          <tr><td><kbd>P</kbd></td><td>Cycle palette</td></tr>
          <tr><td><kbd>F</kbd></td><td>Cycle fractal type</td></tr>
          <tr><td><kbd>S</kbd></td><td>Save PNG</td></tr>
        </table>
        <br>
        <button onclick="document.getElementById('help-overlay').classList.remove('visible')" style="width:100%">Close  [H]</button>
      </div>
    </div>
  </div>

  <div id="sidebar">

    <!-- FRACTAL TYPE -->
    <div class="panel">
      <div class="panel-title">Fractal</div>
      <div class="btn-row" id="fractal-btns">
        <button class="active" data-fractal="mandelbrot">Mandelbrot</button>
        <button data-fractal="julia">Julia</button>
        <button data-fractal="burning_ship">Burning Ship</button>
        <button data-fractal="tricorn">Tricorn</button>
        <button data-fractal="multibrot">Multibrot³</button>
      </div>
      <div id="julia-params">
        <label class="slider-label">
          <span>Re(c)</span><span id="julia-re-val">−0.7269</span>
        </label>
        <input type="range" id="julia-re" min="-2" max="2" step="0.001" value="-0.7269">
        <label class="slider-label">
          <span>Im(c)</span><span id="julia-im-val">+0.1889</span>
        </label>
        <input type="range" id="julia-im" min="-2" max="2" step="0.001" value="0.1889">
      </div>
    </div>

    <!-- PALETTE -->
    <div class="panel">
      <div class="panel-title">Color Palette</div>
      <select id="palette-select">
        <option value="classic">Classic</option>
        <option value="fire">Fire</option>
        <option value="electric">Electric</option>
        <option value="ocean">Ocean</option>
        <option value="neon">Neon</option>
        <option value="matrix">Matrix</option>
        <option value="sunset">Sunset</option>
        <option value="ice">Ice</option>
      </select>
      <div id="palette-preview"></div>
    </div>

    <!-- ITERATIONS -->
    <div class="panel">
      <div class="panel-title">Quality</div>
      <label class="slider-label">
        <span>Max Iterations</span><span id="iter-val">200</span>
      </label>
      <input type="range" id="iter-slider" min="50" max="2000" step="50" value="200">
      <label class="slider-label">
        <span>Supersample</span><span id="ss-val">1×</span>
      </label>
      <input type="range" id="ss-slider" min="1" max="3" step="1" value="1">
    </div>

    <!-- LANDMARKS -->
    <div class="panel">
      <div class="panel-title">Landmarks</div>
      <div id="landmark-list"></div>
    </div>

    <!-- ACTIONS -->
    <div class="panel">
      <div class="panel-title">Actions</div>
      <div class="btn-row">
        <button onclick="resetView()">⟳ Reset</button>
        <button onclick="saveImage()">💾 Save PNG</button>
        <button onclick="document.getElementById('help-overlay').classList.toggle('visible')">? Help</button>
      </div>
    </div>

    <!-- STATS -->
    <div class="panel">
      <div class="panel-title">Stats</div>
      <div class="stat-row"><span class="stat-key">Center Re</span><span class="stat-val" id="s-cx">−0.500000</span></div>
      <div class="stat-row"><span class="stat-key">Center Im</span><span class="stat-val" id="s-cy">+0.000000</span></div>
      <div class="stat-row"><span class="stat-key">Zoom</span><span class="stat-val" id="s-zoom">0.75×</span></div>
      <div class="stat-row"><span class="stat-key">Render time</span><span class="stat-val" id="s-time">—</span></div>
      <div class="stat-row"><span class="stat-key">Canvas</span><span class="stat-val" id="s-size">—</span></div>
    </div>

    <!-- HINTS -->
    <div id="hints">
      <kbd>Scroll</kbd> zoom &nbsp;·&nbsp; <kbd>Drag</kbd> pan<br>
      <kbd>Click</kbd> center &nbsp;·&nbsp; <kbd>R</kbd> reset<br>
      <kbd>↑↓</kbd> iterations &nbsp;·&nbsp; <kbd>P</kbd> palette<br>
      <kbd>S</kbd> save PNG &nbsp;·&nbsp; <kbd>H</kbd> help
    </div>

  </div><!-- /sidebar -->
</div><!-- /main -->

<script>
"use strict";

// ── Palette data from Python ──────────────────────────────────────────────────
const palettes = {{}};
{palettes_js}

const LANDMARKS = {landmarks_js};

// ── State ─────────────────────────────────────────────────────────────────────
let state = {{
  cx:       -0.5,
  cy:       0.0,
  zoom:     0.75,
  maxIter:  200,
  fractal:  "mandelbrot",
  palette:  "classic",
  juliaRe:  -0.7269,
  juliaIm:   0.1889,
  ss:       1,         // supersampling factor
}};

// ── Canvas setup ──────────────────────────────────────────────────────────────
const canvas  = document.getElementById("canvas");
const ctx     = canvas.getContext("2d");
const wrap    = document.getElementById("canvas-wrap");

let renderTimer = null;
let isDragging = false;
let dragStart  = {{ x: 0, y: 0 }};
let dragState  = null;

function resizeCanvas() {{
  canvas.width  = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
  document.getElementById("s-size").textContent = `${{canvas.width}}×${{canvas.height}}`;
  scheduleRender();
}}

// ── Math helpers ──────────────────────────────────────────────────────────────
function screenToWorld(px, py) {{
  const scale  = 2.0 / state.zoom;
  const aspect = canvas.width / canvas.height;
  const x = state.cx + (px / canvas.width  - 0.5) * scale * 2 * aspect;
  const y = state.cy - (py / canvas.height - 0.5) * scale * 2;
  return [x, y];
}}

// ── Fractal computation ───────────────────────────────────────────────────────
function computePixel(zx, zy) {{
  const cx  = state.juliaRe, cy = state.juliaIm;
  const MAX = state.maxIter;
  let x = (state.fractal === "julia") ? zx : 0;
  let y = (state.fractal === "julia") ? zy : 0;
  let px = (state.fractal === "julia") ? cx : zx;
  let py = (state.fractal === "julia") ? cy : zy;

  for (let i = 0; i < MAX; i++) {{
    const x2 = x * x, y2 = y * y;
    if (x2 + y2 > 256) {{
      const logZn = Math.log(x2 + y2) * 0.5;
      const nu    = Math.log(logZn / Math.LN2) / Math.LN2;
      return [i, i + 1 - nu];
    }}
    if (state.fractal === "burning_ship") {{
      const nx = x2 - y2 + px;
      y = 2 * Math.abs(x) * Math.abs(y) + py;
      x = nx;
    }} else if (state.fractal === "tricorn") {{
      const nx = x2 - y2 + px;
      y = -2 * x * y + py;
      x = nx;
    }} else if (state.fractal === "multibrot") {{
      const r     = Math.sqrt(x2 + y2);
      const theta = Math.atan2(y, x) * 3;
      const r3    = r * r * r;
      x = r3 * Math.cos(theta) + px;
      y = r3 * Math.sin(theta) + py;
    }} else {{
      const nx = x2 - y2 + px;
      y = 2 * x * y + py;
      x = nx;
    }}
  }}
  return [MAX, MAX];
}}

// ── Color mapping ─────────────────────────────────────────────────────────────
function lerp(a, b, t) {{ return a + (b - a) * t; }}

function samplePalette(t) {{
  const stops = palettes[state.palette];
  if (!stops) return [0, 255, 255];
  t = Math.max(0, Math.min(1, t));
  const pos = t * (stops.length - 1);
  const idx = Math.min(Math.floor(pos), stops.length - 2);
  const frac = pos - idx;
  const [r1, g1, b1] = stops[idx];
  const [r2, g2, b2] = stops[idx + 1];
  return [
    Math.round(lerp(r1, r2, frac)),
    Math.round(lerp(g1, g2, frac)),
    Math.round(lerp(b1, b2, frac)),
  ];
}}

function iterToRGB(itr, smooth) {{
  if (itr >= state.maxIter) return [0, 0, 0];
  let t = smooth / state.maxIter;
  t = Math.sqrt(t);
  t = (t * 3.5) % 1.0;
  return samplePalette(t);
}}

// ── Chunked render ────────────────────────────────────────────────────────────
let renderGen = null;
const CHUNK_ROWS = 8;   // rows per animation frame

function* renderGenerator(snap) {{
  const W = canvas.width,  H = canvas.height;
  const ss  = snap.ss;
  const RW  = Math.ceil(W / ss), RH = Math.ceil(H / ss);
  const scale  = 2.0 / snap.zoom;
  const aspect = W / H;
  const xMin = snap.cx - scale * aspect;
  const yMax = snap.cy + scale;
  const xRange = scale * 2 * aspect;
  const yRange = scale * 2;

  const imgData = ctx.createImageData(W, H);
  const d = imgData.data;

  for (let rRow = 0; rRow < RH; rRow += CHUNK_ROWS) {{
    const endRow = Math.min(rRow + CHUNK_ROWS, RH);

    for (let rR = rRow; rR < endRow; rR++) {{
      for (let rC = 0; rC < RW; rC++) {{
        const re = xMin + (rC + 0.5) / RW * xRange;
        const im = yMax - (rR + 0.5) / RH * yRange;
        const [itr, smooth] = computePixel(re, im);
        const [r, g, b] = iterToRGB(itr, smooth);

        // Fill ss×ss block of actual pixels
        for (let dy = 0; dy < ss && rR * ss + dy < H; dy++) {{
          for (let dx = 0; dx < ss && rC * ss + dx < W; dx++) {{
            const idx = ((rR * ss + dy) * W + (rC * ss + dx)) * 4;
            d[idx]     = r;
            d[idx + 1] = g;
            d[idx + 2] = b;
            d[idx + 3] = 255;
          }}
        }}
      }}
    }}

    ctx.putImageData(imgData, 0, 0);
    const pct = (endRow / RH * 100).toFixed(0);
    document.getElementById("progress-bar").style.width = pct + "%";
    yield; // yield control back to the event loop
  }}

  document.getElementById("progress-bar").style.width = "0%";
  document.getElementById("rendering-badge").style.display = "none";
}}

function scheduleRender(delay = 60) {{
  if (renderTimer) clearTimeout(renderTimer);
  renderTimer = setTimeout(startRender, delay);
}}

function startRender() {{
  const t0 = performance.now();
  document.getElementById("rendering-badge").style.display = "block";

  const snap = {{ ...state }};
  renderGen  = renderGenerator(snap);

  function step() {{
    if (!renderGen) return;
    const res = renderGen.next();
    if (res.done) {{
      const ms = (performance.now() - t0).toFixed(0);
      document.getElementById("s-time").textContent = ms + " ms";
      renderGen = null;
    }} else {{
      requestAnimationFrame(step);
    }}
  }}
  requestAnimationFrame(step);

  updateStats();
}}

// ── Stats & UI sync ───────────────────────────────────────────────────────────
function updateStats() {{
  document.getElementById("s-cx").textContent   = state.cx.toFixed(8);
  document.getElementById("s-cy").textContent   = (state.cy >= 0 ? "+" : "") + state.cy.toFixed(8);
  document.getElementById("s-zoom").textContent = state.zoom.toFixed(2) + "×";
  document.getElementById("iter-val").textContent = state.maxIter;
  document.getElementById("ss-val").textContent   = state.ss + "×";
}}

// ── Zoom ──────────────────────────────────────────────────────────────────────
function zoomAt(screenX, screenY, factor) {{
  const [wx, wy] = screenToWorld(screenX, screenY);
  state.zoom *= factor;
  // Adjust center so the world point stays under cursor
  const scale  = 2.0 / state.zoom;
  const aspect = canvas.width / canvas.height;
  state.cx = wx - (screenX / canvas.width  - 0.5) * scale * 2 * aspect;
  state.cy = wy + (screenY / canvas.height - 0.5) * scale * 2;
  scheduleRender(40);
}}

// ── Interaction ───────────────────────────────────────────────────────────────
canvas.addEventListener("wheel", e => {{
  e.preventDefault();
  const factor = e.deltaY < 0 ? 1.25 : 0.8;
  zoomAt(e.offsetX, e.offsetY, factor);
}}, {{ passive: false }});

canvas.addEventListener("mousedown", e => {{
  isDragging = true;
  dragStart = {{ x: e.clientX, y: e.clientY }};
  dragState = {{ cx: state.cx, cy: state.cy }};
  canvas.style.cursor = "grabbing";
}});

window.addEventListener("mousemove", e => {{
  // Coordinate display
  const rect = canvas.getBoundingClientRect();
  const px = e.clientX - rect.left, py = e.clientY - rect.top;
  const [wx, wy] = screenToWorld(px, py);
  document.getElementById("coords").textContent =
    `Re: ${{wx.toFixed(8)}}  Im: ${{(wy >= 0 ? "+" : "")}}${{wy.toFixed(8)}}  |  Zoom: ${{state.zoom.toFixed(3)}}×`;

  if (!isDragging) return;
  const dx = (e.clientX - dragStart.x) / canvas.width;
  const dy = (e.clientY - dragStart.y) / canvas.height;
  const scale  = 2.0 / state.zoom;
  const aspect = canvas.width / canvas.height;
  state.cx = dragState.cx - dx * scale * 2 * aspect;
  state.cy = dragState.cy + dy * scale * 2;
  scheduleRender(20);
}});

window.addEventListener("mouseup", () => {{
  isDragging = false;
  canvas.style.cursor = "crosshair";
}});

canvas.addEventListener("dblclick", e => {{
  zoomAt(e.offsetX, e.offsetY, 2.5);
}});

// ── Keyboard shortcuts ────────────────────────────────────────────────────────
const FRACTAL_CYCLE = ["mandelbrot","julia","burning_ship","tricorn","multibrot"];
const PALETTE_CYCLE = Object.keys(palettes);

window.addEventListener("keydown", e => {{
  if (e.target !== document.body && e.target !== document.documentElement) return;
  const key = e.key.toLowerCase();
  if (key === "r") resetView();
  else if (key === "h") document.getElementById("help-overlay").classList.toggle("visible");
  else if (key === "s") saveImage();
  else if (key === "p") {{
    const i = PALETTE_CYCLE.indexOf(state.palette);
    state.palette = PALETTE_CYCLE[(i + 1) % PALETTE_CYCLE.length];
    document.getElementById("palette-select").value = state.palette;
    updatePalettePreview();
    scheduleRender(30);
  }} else if (key === "f") {{
    const i = FRACTAL_CYCLE.indexOf(state.fractal);
    setFractal(FRACTAL_CYCLE[(i + 1) % FRACTAL_CYCLE.length]);
  }} else if (key === "arrowup") {{
    state.maxIter = Math.min(2000, state.maxIter + 50);
    document.getElementById("iter-slider").value = state.maxIter;
    scheduleRender();
  }} else if (key === "arrowdown") {{
    state.maxIter = Math.max(50, state.maxIter - 50);
    document.getElementById("iter-slider").value = state.maxIter;
    scheduleRender();
  }} else if (key === "+" || key === "=") {{
    zoomAt(canvas.width / 2, canvas.height / 2, 1.5);
  }} else if (key === "-") {{
    zoomAt(canvas.width / 2, canvas.height / 2, 1 / 1.5);
  }}
}});

// ── Control panel bindings ────────────────────────────────────────────────────
function setFractal(name) {{
  state.fractal = name;
  document.querySelectorAll("#fractal-btns button").forEach(b => {{
    b.classList.toggle("active", b.dataset.fractal === name);
  }});
  const jp = document.getElementById("julia-params");
  if (name === "julia") jp.classList.add("visible");
  else jp.classList.remove("visible");
  scheduleRender();
}}

document.querySelectorAll("#fractal-btns button").forEach(btn => {{
  btn.addEventListener("click", () => setFractal(btn.dataset.fractal));
}});

document.getElementById("palette-select").addEventListener("change", e => {{
  state.palette = e.target.value;
  updatePalettePreview();
  scheduleRender(30);
}});

document.getElementById("iter-slider").addEventListener("input", e => {{
  state.maxIter = +e.target.value;
  document.getElementById("iter-val").textContent = state.maxIter;
  scheduleRender(200);
}});

document.getElementById("ss-slider").addEventListener("input", e => {{
  state.ss = +e.target.value;
  document.getElementById("ss-val").textContent = state.ss + "×";
  scheduleRender(100);
}});

document.getElementById("julia-re").addEventListener("input", e => {{
  state.juliaRe = +e.target.value;
  document.getElementById("julia-re-val").textContent = (+e.target.value).toFixed(4);
  scheduleRender(100);
}});

document.getElementById("julia-im").addEventListener("input", e => {{
  state.juliaIm = +e.target.value;
  document.getElementById("julia-im-val").textContent =
    (+e.target.value >= 0 ? "+" : "") + (+e.target.value).toFixed(4);
  scheduleRender(100);
}});

// ── Landmarks ─────────────────────────────────────────────────────────────────
function buildLandmarks() {{
  const list = document.getElementById("landmark-list");
  for (const [name, loc] of Object.entries(LANDMARKS)) {{
    const btn = document.createElement("button");
    btn.textContent = name;
    btn.addEventListener("click", () => {{
      state.cx      = loc.cx;
      state.cy      = loc.cy;
      state.zoom    = loc.zoom;
      state.maxIter = loc.max_iter || 200;
      state.fractal = "mandelbrot";
      document.getElementById("iter-slider").value = state.maxIter;
      setFractal("mandelbrot");
      scheduleRender(0);
    }});
    list.appendChild(btn);
  }}
}}

function resetView() {{
  state.cx   = -0.5;
  state.cy   = 0.0;
  state.zoom = 0.75;
  scheduleRender(0);
}}

// ── Palette preview strip ─────────────────────────────────────────────────────
function updatePalettePreview() {{
  const stops = palettes[state.palette] || [];
  const gradient = stops.map((c, i) => {{
    const pct = (i / (stops.length - 1) * 100).toFixed(0);
    return `rgb(${{c[0]}},${{c[1]}},${{c[2]}}) ${{pct}}%`;
  }}).join(", ");
  document.getElementById("palette-preview").style.background =
    `linear-gradient(to right, ${{gradient}})`;
}}

// ── Save PNG ──────────────────────────────────────────────────────────────────
function saveImage() {{
  const link = document.createElement("a");
  link.download = `mandelbrot-voyage-${{state.cx.toFixed(4)}}-${{state.zoom.toFixed(0)}}.png`;
  link.href = canvas.toDataURL("image/png");
  link.click();
}}

// ── Resize observer ───────────────────────────────────────────────────────────
new ResizeObserver(resizeCanvas).observe(wrap);

// ── Init ──────────────────────────────────────────────────────────────────────
buildLandmarks();
updatePalettePreview();
resizeCanvas();
</script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
